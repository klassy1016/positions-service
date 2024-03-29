from fastapi import APIRouter, Request
from app.models.position import PnlLog, AggregatedPnl
from app.crud.positions import get_db_pnls, get_strat_pnl


pnl_router = APIRouter(prefix='/pnl')


@pnl_router.get("/log", response_model=PnlLog, tags=["pnl_log"])
def get_pnl_log():
    return get_db_pnls()


@pnl_router.get("/pnl", response_model=AggregatedPnl, tags=["pnl_log"])
def filtered_pnl(req: Request):
    filter_args = dict(req.query_params)
    pnls = get_db_pnls(filter_args)
    pnl_sum = 0.0
    for pnl in pnls.pnl_log:
        pnl_sum += pnl.pnl
    return AggregatedPnl(pnl=pnl_sum, filtered_by=filter_args)

@pnl_router.get("/strat_realized_pnl/{strategy}", tags=["pnl_log"])
def get_strat_realized_pnl(strategy: str):
    return get_strat_pnl(strategy)

@pnl_router.get("/pnl_by_date", response_model=AggregatedPnl, tags=["pnl_log"])
def pnl_by_date(req: Request):
    filter_args = dict(req.query_params)
    pnls = get_db_pnls(filter_args)
    pnl_sum = 0.0
    for pnl in pnls.pnl_log:
        pnl_sum += pnl.pnl
    return AggregatedPnl(pnl=pnl_sum, filtered_by=filter_args)