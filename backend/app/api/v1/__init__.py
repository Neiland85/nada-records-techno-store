     """
API v1 router configuration.
Centralizes all v1 API endpoints.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, users, music, upload

# Create the main API router for v1
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(
    auth.router,
    prefix="/auth",
    tags=["authentication"]
)

api_router.include_router(
    users.router,
    prefix="/users",
    tags=["users"]
)

api_router.include_router(
    music.router,
    prefix="/music",
    tags=["music"]
)

api_router.include_router(
    upload.router,
    prefix="/upload",
    tags=["upload"]
)
