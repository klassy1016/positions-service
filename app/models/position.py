from typing import List, Optional
from app.models.dbmodel import DateTimeModelMixin, DBModelMixin

from pydantic import BaseConfig, BaseModel

class Position(BaseModel):
    id: str = ""
    trader: str = ""
    quantity: float = 0.0
    broker: str = ""
    strategy: str = ""
    portfolio: str = ""
    asset_type: str = ""
    entry_date: str = ""
    exit_date: str = None

class MultiPositionModel(BaseModel):
    positions: List[Position]

class PositionsInDB(DBModelMixin, MultiPositionModel):
    pass

class CreatedPosition(BaseModel):
    position: Position
