from fastapi import FastAPI
from app.db import mongo_db

from app.api.v1.api import router as api_router

app = FastAPI(title='Positions Service')

app.add_event_handler("startup", mongo_db.connect_client)
app.add_event_handler("shutdown", mongo_db.close_client)

app.include_router(api_router, prefix="/v1")
