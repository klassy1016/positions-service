from fastapi import FastAPI
from app.db import mongo_db
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_422_UNPROCESSABLE_ENTITY

from app.api.v1.api import router as api_router

app = FastAPI(title='Positions Service')

app.add_event_handler("startup", mongo_db.connect_client)
app.add_event_handler("shutdown", mongo_db.close_client)

# app.add_exception_handler(HTTPException, http_error_handler)
# app.add_exception_handler(HTTP_422_UNPROCESSABLE_ENTITY, http_422_error_handler)

app.include_router(api_router, prefix="/v1")