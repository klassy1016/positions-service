from fastapi import APIRouter, Request
from app.models.position import PositionList
from app.crud.positions import get_db_positions #, delete_all


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


@position_router.get("/positions_by_filter", response_model=PositionList, tags=["positions_by_filter"])
def positions_by_filter(req: Request):
    filter_args = dict(req.query_params)
    return query_positions(query=filter_args)

# @position_router.get("/delete_all_positions", response_model=PositionList, tags=["active_positions"])
# def delete_all_positions():
#     delete_all()