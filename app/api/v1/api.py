from fastapi import APIRouter

from app.api.v1.endpoints.positions import position_router
from app.api.v1.endpoints.pnl import pnl_router
from app.api.v1.endpoints.trade import trade_router

router = APIRouter()
router.include_router(position_router)
router.include_router(pnl_router)
router.include_router(trade_router)