from fastapi import APIRouter
from app.models.position import PositionList
from app.crud.positions import get_db_positions


position_router = APIRouter(prefix='/positions')


def query_positions(query={}):
    positions_list = get_db_positions(query=query)
    return PositionList(positions=positions_list)


@position_router.get("/active_positions", response_model=PositionList, tags=["active_positions"])
def active_positions():
    active_query = {'active': True}
    return query_positions(query=active_query)

@position_router.get("/positions", response_model=PositionList, tags=["positions"])
def positions():
    return query_positions()

