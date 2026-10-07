"""
starting the fastAPI app.
"""
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from db.db_operations import engine
import db.schemas as models
from api import router as api_router

app = FastAPI(
    title="RouteFlowAI",
    description="AI-powered routing and recommendation pipelines",
    version="0.1.0"
)

# Enable CORS for local development and browser access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Connecting the api_router to the app
app.include_router(
    api_router,
    prefix="/api/v1",
    tags=["Core API"]
)

# Static files directory
STATIC_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "static")
os.makedirs(STATIC_DIR, exist_ok=True)

# Mount static files directory
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/", include_in_schema=False)
async def serve_index():
    index_file = os.path.join(STATIC_DIR, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {"message": "RouteFlowAI API is active. UI not found."}

# Creates the tables in Postgres if they don't exist yet
models.Base.metadata.create_all(bind=engine)

