"""API v1 package."""
from fastapi import APIRouter

from app.api.v1.endpoints import auth, catalog, upload, health

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(catalog.router, prefix="/catalog", tags=["catalog"])
api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
