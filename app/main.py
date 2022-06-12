from fastapi import FastAPI

from app.db.mongodb_utils import connect_to_mongo, close_mongo_connection
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.api.v1.api import router as api_router

app = FastAPI(title='Positions Service')

app.add_event_handler("startup", connect_to_mongo)
app.add_event_handler("shutdown", close_mongo_connection)

# app.add_exception_handler(HTTPException, http_error_handler)
# app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.include_router(api_router, prefix="/v1")