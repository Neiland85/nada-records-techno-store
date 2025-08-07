"""Simplified FastAPI application for Vercel deployment."""

import os
import sys
from pathlib import Path

# Add the backend directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Create a simplified FastAPI app for Vercel
app = FastAPI(
    title="Nada Records Techno Store API",
    version="1.0.0",
    description="API para tienda de música electrónica Nada Records"
)

# Configure CORS for Vercel deployment
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://localhost:3000",
        "https://*.vercel.app",
        "https://nadarecords.com",
        "https://www.nadarecords.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Nada Records Techno Store API",
        "version": "1.0.0",
        "status": "running",
        "deployment": "vercel",
        "docs_url": "/docs",
        "api_prefix": "/api/v1"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": "Nada Records API",
        "version": "1.0.0",
        "deployment_platform": "vercel",
        "environment": "production" if os.getenv("VERCEL_ENV") == "production" else "preview",
        "region": os.getenv("VERCEL_REGION", "unknown"),
        "endpoints": {
            "auth": "/api/v1/auth",
            "catalog": "/api/v1/catalog", 
            "upload": "/api/v1/upload",
            "health": "/api/v1/health"
        }
    }


@app.get("/api/v1/health/database")
async def database_health():
    """Database health check."""
    try:
        database_url = os.getenv("DATABASE_URL")
        if not database_url:
            return JSONResponse(
                status_code=503,
                content={
                    "status": "unhealthy",
                    "message": "Database URL not configured",
                    "component": "database"
                }
            )
        
        # Simplified database check
        return {
            "status": "healthy",
            "component": "database",
            "configured": True,
            "message": "Database connection configured"
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "component": "database",
                "error": str(e)
            }
        )


@app.get("/api/v1/health/email")
async def email_health():
    """Email service health check."""
    try:
        sendgrid_key = os.getenv("SENDGRID_API_KEY")
        return {
            "status": "healthy" if sendgrid_key else "warning",
            "component": "email",
            "configured": bool(sendgrid_key),
            "provider": "SendGrid",
            "message": "Email service configured" if sendgrid_key else "Email service not configured"
        }
    
    except Exception as e:
        return JSONResponse(
            status_code=503,
            content={
                "status": "unhealthy",
                "component": "email",
                "error": str(e)
            }
        )


@app.get("/api/v1/config")
async def get_config():
    """Get application configuration."""
    return {
        "app_name": "Nada Records Techno Store API",
        "version": "1.0.0",
        "environment": os.getenv("VERCEL_ENV", "development"),
        "region": os.getenv("VERCEL_REGION", "unknown"),
        "features": {
            "authentication": True,
            "catalog": True,
            "upload": False,  # Disabled for Vercel limitations
            "payments": bool(os.getenv("STRIPE_SECRET_KEY")),
            "email": bool(os.getenv("SENDGRID_API_KEY")),
            "database": bool(os.getenv("DATABASE_URL"))
        },
        "limits": {
            "file_upload": "Disabled on Vercel",
            "audio_processing": "Disabled on Vercel",
            "websockets": "Limited on Vercel"
        }
    }


# Try to import full application if dependencies are available
try:
    from app.main import app as full_app
    from app.api.v1 import api_router
    
    # Include API routes if available
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/api/v1/status")
    async def full_api_status():
        return {
            "status": "full_api_loaded",
            "message": "All API endpoints are available",
            "features": "complete"
        }

except ImportError as e:
    @app.get("/api/v1/status")
    async def limited_api_status():
        return {
            "status": "limited_api",
            "message": "Running in limited mode due to missing dependencies",
            "missing_features": ["audio_upload", "audio_processing", "advanced_search"],
            "error": str(e)
        }


# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={
            "error": "Endpoint not found",
            "message": "The requested endpoint does not exist",
            "available_endpoints": {
                "docs": "/docs",
                "health": "/health",
                "api": "/api/v1",
                "config": "/api/v1/config"
            }
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "deployment": "vercel",
            "support": "Please check the logs or contact support"
        }
    )


# Vercel handler
def handler(request, context):
    """Vercel handler function."""
    return app


# For development
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=int(os.getenv("PORT", 8000))
    )