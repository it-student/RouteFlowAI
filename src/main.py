"""
starting the fastAPI app.
"""
from typing import Annotated, List

from fastapi import FastAPI
from db.db_operations import engine
import db.schemas as models
from api import router as api_router

app = FastAPI()

# Connecting the api_router to the app
app.include_router(
    api_router,
    prefix="/api/v1",
    tags=["Core API"]
)

# Creates the tables in Postgres if they don't exist yet
models.Base.metadata.create_all(bind=engine)
