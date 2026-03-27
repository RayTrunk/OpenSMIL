from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api import api_router
from app.core.config import settings
from app.core.db import init_db

# Ensure models are imported for metadata registration
from app.models import user, player, media, playlist

import os

app = FastAPI(
    title="OpenSMIL Signage Backend",
    description="Scalable Digital Signage backend compliant with SMIL 3.0",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    init_db()

# Set CORS origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, this should be restricted
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount Static and Media folders
if not os.path.exists(settings.MEDIA_LOCAL_PATH):
    os.makedirs(settings.MEDIA_LOCAL_PATH)

app.mount("/media", StaticFiles(directory=settings.MEDIA_LOCAL_PATH), name="media")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(api_router, prefix="/api/v1")

# Initialize database
init_db()

@app.get("/")
def read_root():
    return {
        "message": "Welcome to OpenSMIL Signage API",
        "logo_url": "/static/logo.png",
        "docs_url": "/docs"
    }
