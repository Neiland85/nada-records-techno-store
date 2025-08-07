"""Main FastAPI application entry point."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API para tienda de música electrónica Nada Records"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "https://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint."""
    return {
        "message": "Nada Records Techno Store API",
        "version": settings.APP_VERSION,
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Detailed health check."""
    return {
        "status": "healthy",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "sendgrid_configured": bool(settings.SENDGRID_API_KEY.get_secret_value()),
        "frontend_url": str(settings.FRONTEND_URL)
    }


@app.get("/api/v1/test-email")
async def test_email_config():
    """Test email configuration endpoint."""
    from app.core.email import email_settings
    
    return {
        "sendgrid_configured": bool(email_settings.sendgrid_api_key),
        "from_email": email_settings.sendgrid_from_email,
        "from_name": email_settings.sendgrid_from_name,
        "email_service": "SendGrid",
        "status": "configured" if email_settings.sendgrid_api_key else "not_configured"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
