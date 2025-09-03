"""
API v1 router.
"""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, music, upload, users

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(music.router, prefix="/music", tags=["music"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
