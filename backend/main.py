"""Main FastAPI application entry point."""

import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.core.config import settings
from app.api.v1 import api_router

# Create rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para tienda de música electrónica Nada Records",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
)

# Add rate limiting
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Configure CORS
allowed_origins = [
    "http://localhost:3000",
    "https://localhost:3000",
    str(settings.FRONTEND_URL),
]

# Add Vercel preview URLs and production URLs
if not settings.DEBUG:
    allowed_origins.extend([
        "https://*.vercel.app",
        "https://nadarecords.com",
        "https://www.nadarecords.com",
    ])

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Nada Records Techno Store API",
        "version": settings.APP_VERSION,
        "status": "running",
        "docs_url": "/docs" if settings.DEBUG else "disabled",
        "api_prefix": settings.API_V1_STR
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "debug_mode": settings.DEBUG,
        "database_configured": bool(settings.DATABASE_URL),
        "redis_configured": bool(settings.REDIS_URL),
        "sendgrid_configured": bool(settings.SENDGRID_API_KEY.get_secret_value()),
        "storage_configured": bool(settings.B2_KEY_ID.get_secret_value()),
        "stripe_configured": bool(settings.STRIPE_SECRET_KEY.get_secret_value()),
        "frontend_url": str(settings.FRONTEND_URL),
        "api_endpoints": {
            "auth": f"{settings.API_V1_STR}/auth",
            "catalog": f"{settings.API_V1_STR}/catalog", 
            "upload": f"{settings.API_V1_STR}/upload",
            "health": f"{settings.API_V1_STR}/health"
        }
    }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {
        "error": "Endpoint not found",
        "message": "The requested endpoint does not exist",
        "available_endpoints": {
            "docs": "/docs" if settings.DEBUG else "disabled",
            "health": "/health",
            "api": settings.API_V1_STR
        }
    }


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {
        "error": "Internal server error",
        "message": "An unexpected error occurred",
        "debug_info": str(exc) if settings.DEBUG else "Contact support"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000)),
        reload=settings.DEBUG
    )
