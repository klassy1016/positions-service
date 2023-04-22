from bson import ObjectId
import math
from datetime import datetime
from fastapi.encoders import jsonable_encoder

from app.models.position import (
    LoggedTrade,
    Pnl,
    Position,
    Trade,
    PnlLog
)
from app.db import mongo_db
from app.core.config import raw_positions_collection_name, trade_collection_name, pnl_collection_name


def build_position_query(position: Position):
    query = {
        "id": position.id,
        "trader": position.trader,
        "pfo": position.pfo,
        "strategy": position.strategy,
    }
    return query


def log_trade(trade: Trade) -> LoggedTrade:
    position = get_position(trade_query=build_position_query(trade.position))
    if not position:  # First time trading, simply add position and log trade
        add_position_to_db(trade.position)
        # log trade
        added_trade, status = add_trade_to_db(trade)
        return LoggedTrade(trade=added_trade, status=status)
    else:
        # We're trading a current position, must update position and pnl
        pnl = update_position(trade, position)
        # Log realized pnl from trade
        if pnl:
            log_pnl(trade, pnl)
        added_trade, status = add_trade_to_db(trade)
        return LoggedTrade(trade=added_trade, status=status)


def get_db_pnls(query={}):
    pnl_query = {}
    for key in query.keys():
        pnl_query['trade.position.'+key] = query[key]
    pnls = mongo_db.query(collection_name=pnl_collection_name, query=pnl_query)
    return PnlLog(pnl_log=pnls)


def add_trade_to_db(trade: Trade) -> Trade:
    trade_doc = jsonable_encoder(trade)
    mongo_db.insert(collection_name=trade_collection_name, data=trade_doc)

    return Trade(**trade_doc, created_at=ObjectId(trade_doc["_id"]).generation_time), "SUCCESS"


def add_position_to_db(position: Position):
    position_doc = jsonable_encoder(position)
    mongo_db.insert(collection_name=raw_positions_collection_name, data=position_doc)

    return Position(
        **position_doc,
        created_at=ObjectId(position_doc["_id"]).generation_time,
    )


def get_db_trade_log(query = {}):
    trades = mongo_db.query(collection_name=trade_collection_name, query=query)
    return trades


def get_position(trade_query):
    position_doc = mongo_db.query_most_recent(collection_name=raw_positions_collection_name, query=trade_query, time_field='last_trade_time')
    if not position_doc:
        return None
    else:
        return Position(**position_doc)


def get_db_positions(query = {}):
    positions = mongo_db.query(collection_name=raw_positions_collection_name, query=query)
    return positions


def log_pnl(trade: Trade, pnl: float, ):
    pnl_model = Pnl(pnl=pnl, trade=trade)
    mongo_db.insert(collection_name=pnl_collection_name, data=jsonable_encoder(pnl_model))
    return


def close_position(trade: Trade):
    mongo_db.delete(collection_name=raw_positions_collection_name, query=build_position_query(trade.position))

# def delete_all():
#     mongo_db.delete(collection_name=raw_positions_collection_name, query={})


def calculate_new_cost_basis_quantity(trade: Trade, position: Position):
    trade_quantity = trade.position.quantity
    trade_cost_basis = trade.position.cost_basis
    original_quantity = position.quantity
    original_cost_basis = position.cost_basis
    new_quantity = trade_quantity + original_quantity
    if original_quantity > 0: # Currently long
        if trade_quantity < 0: # Selling off
            trade_quantity = math.fabs(trade_quantity) # convert quantity into a positive number
            if new_quantity == 0:
                pnl = trade_cost_basis - original_cost_basis
                return pnl, 0, new_quantity
            else:
                pnl = trade_quantity * (trade_cost_basis - original_cost_basis)
                new_cost_basis = original_cost_basis
                return pnl, new_cost_basis, new_quantity
        else: # Buying more
            new_cost_basis = ((trade_cost_basis * trade_quantity) + (original_cost_basis * original_quantity)) / (new_quantity)
            return 0.0, new_cost_basis, new_quantity

    if original_quantity < 0:  # Currently short
        if trade_quantity < 0:  # Shorting More
            if new_quantity == 0:
                pnl = original_cost_basis - trade_cost_basis
                return pnl, 0, new_quantity
            else:
                pnl = trade_quantity * (original_cost_basis - trade_cost_basis)
                new_cost_basis = original_cost_basis
                return pnl, new_cost_basis, new_quantity
        else:  # Buying out
            if new_quantity == 0:
                pnl = original_cost_basis - trade_cost_basis
                return pnl, 0, new_quantity
            else:
                new_cost_basis = ((trade_cost_basis * trade_quantity) + (original_cost_basis * original_quantity)) /\
                                 math.fabs(new_quantity)
                return 0.0, new_cost_basis, new_quantity


def update_position(trade: Trade, position: Position):
    pnl, new_basis, new_quantity = calculate_new_cost_basis_quantity(trade, position)

    if new_quantity == 0:
        mongo_db.delete(collection_name=raw_positions_collection_name,
                        query=build_position_query(position))
        return pnl
    position_updates = {
        "$set": {'quantity': new_quantity,
                 'cost_basis': new_basis,
                 'active': bool(new_quantity != 0),
                 'last_trade_time': datetime.now(),
                 'exit_date': (datetime.today() if new_quantity == 0 else None)}
    }

    mongo_db.update(collection_name=raw_positions_collection_name,
                    query=build_position_query(position),
                    update_fields=position_updates)
    return pnl
