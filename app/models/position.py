from datetime import datetime, date
from pydantic import BaseModel
from typing import List, Optional


class Position(BaseModel):
    id: str = ""
    trader: str = ""
    broker: str = ""
    exchange: str = ""
    pfo: str = ""
    pfo_group: str = ""
    strategy: str = ""
    asset_type: str = ""
    quantity: float = 0.0
    cost_basis: float = 0.0
    outstanding_fees: float = 0.0  # Fees incurred at entry that haven't yet been realized on pnl
    entry_date: date = date.today()
    exit_date: Optional[date] = None
    pricing_source: str = "eod_historical"
    last_trade_time: datetime = datetime.now()
    active: bool = True


class PositionList(BaseModel):
    positions: List[Position] = []


class Trade(BaseModel):
    position: Position
    trade_time: datetime = datetime.now()


class LoggedTrade(BaseModel):
    trade: Trade
    status: str = ""


class TradeLog(BaseModel):
    trades: List[Trade]


class Pnl(BaseModel):
    pnl: float = 0.0
    pnl_type: str = 'dollar'
    trade: Trade

class ExitDateStrategy(BaseModel):
    exit_date: date = None
    stategy_name: str = ''

class AggregatedPnl(BaseModel):
    pnl: float = 0.0,
    pnl_type: str = 'dollar'
    filtered_by: dict = {}


class PnlLog(BaseModel):
    pnl_log: List[Pnl]

class StrategyPnl(BaseModel):
    strategy_id: str = ""
    pnl: float = 0.0


