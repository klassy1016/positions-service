from fastapi import APIRouter
from app.models.position import LoggedTrade, Trade,  TradeLog
from app.crud.positions import get_db_trade_log, log_trade


trade_router = APIRouter(prefix='/trade')


@trade_router.post("/post_trade", response_model=LoggedTrade, tags=["post_trade"])
def post_trade(trade: Trade):
    return log_trade(trade)


@trade_router.get("/trade_log", response_model=TradeLog, tags=["trade_log"])
def get_trade_log():
    trade_log = get_db_trade_log()
    return TradeLog(trades=trade_log)

