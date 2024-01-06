from fastapi import APIRouter, Request, Body
from app.models.position import PositionList, ExitDateStrategy
from app.crud.positions import get_db_positions, delete_all
from typing import Any, Dict


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

@position_router.get("/positions_to_exit", response_model=PositionList, tags=["positions_by_filter"])
def positions_to_exit(req: Request):
    filter_args = dict(req.query_params)
    dt = filter_args['exit_date']
    strat = filter_args['strategy']
    query = {"exit_date": {"$lte": dt}, "strategy": strat}
    return query_positions(query=query)

@position_router.get("/delete_all_positions", response_model=PositionList, tags=["active_positions"])
def delete_all_positions():
    delete_all()
    return PositionList()
