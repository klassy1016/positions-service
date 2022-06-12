from typing import List, Optional
from bson import ObjectId
from datetime import datetime

from app.models.position import (
    Position,
    MultiPositionModel,
)
from app.db.mongodb import AsyncIOMotorClient
from app.core.config import database_name, raw_positions_collection_name


async def add_trade_to_db(conn: AsyncIOMotorClient,
                          position: Position) -> Position:
    position_doc = position.dict()
    position_doc["update_time"] = datetime.now()
    await conn[database_name][raw_positions_collection_name].insert_one(position_doc)

    return Position(
        **position_doc,
        created_at=ObjectId(position_doc["_id"]).generation_time,
    )

async def get_all_positions(conn: AsyncIOMotorClient):
    positions = await conn[database_name][raw_positions_collection_name].find({}).to_list(length=100)
    return positions