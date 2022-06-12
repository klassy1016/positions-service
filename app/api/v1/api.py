from fastapi import APIRouter

from .endpoints.positions import router as positions_router

router = APIRouter()
router.include_router(positions_router)