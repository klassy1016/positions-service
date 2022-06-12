from fastapi import APIRouter, Body, Depends, Path, Query
from app.models.position import Position, MultiPositionModel, CreatedPosition
from app.db.mongodb import AsyncIOMotorClient, get_database
from app.crud.positions import add_trade_to_db, get_all_positions
from app.core.utils import create_aliased_response



router = APIRouter()

@router.post("/add_trade")
async def add_trade(trade: Position,
                    db: AsyncIOMotorClient = Depends(get_database)):
    added_trade = await add_trade_to_db(db, trade)
    return create_aliased_response(CreatedPosition(position=added_trade))


@router.get("/positions", response_model=Position, tags=["articles"])
async def get_positions(db: AsyncIOMotorClient = Depends(get_database)):
    positions = await get_all_positions(db)
    return create_aliased_response(MultiPositionModel(positions=positions))