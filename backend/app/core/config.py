"""
Core configuration module for the FastAPI music store.
Uses Pydantic Settings for environment variable validation and type safety.
"""
from typing import List, Optional, Dict, Any
from datetime import timedelta
from functools import lru_cache

from pydantic import BaseSettings, validator, PostgresDsn, RedisDsn, EmailStr, HttpUrl
from pydantic.types import SecretStr


class Settings(BaseSettings):
    """Application settings with environment variable support."""
    
    # Application settings
    APP_NAME: str = "Music Store API"
    APP_VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False
    
    # Server settings
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    WORKERS: int = 1
    
    # Database settings
    DATABASE_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 40
    DATABASE_POOL_TIMEOUT: int = 30
    
    # Redis settings
    REDIS_URL: RedisDsn
    REDIS_POOL_SIZE: int = 10
    REDIS_DECODE_RESPONSES: bool = True
    
    # Storage configuration (Backblaze B2)
    B2_KEY_ID: SecretStr
    B2_APPLICATION_KEY: SecretStr
    B2_BUCKET_NAME: str
    B2_BUCKET_ID: str
    B2_ENDPOINT_URL: Optional[HttpUrl] = None
    
    # Storage buckets
    AUDIO_BUCKET: str = "audio-files"
    COVER_BUCKET: str = "album-covers"
    PREVIEW_BUCKET: str = "track-previews"
    
    # Stripe configuration
    STRIPE_PUBLISHABLE_KEY: str
    STRIPE_SECRET_KEY: SecretStr
    STRIPE_WEBHOOK_SECRET: SecretStr
    STRIPE_SUCCESS_URL: HttpUrl
    STRIPE_CANCEL_URL: HttpUrl
    
    # JWT settings
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_EMAIL_VERIFICATION_EXPIRE_HOURS: int = 24
    JWT_PASSWORD_RESET_EXPIRE_HOURS: int = 1
    
    # Audio processing settings
    SUPPORTED_AUDIO_FORMATS: List[str] = ["mp3", "wav", "flac", "aac", "ogg"]
    MAX_AUDIO_FILE_SIZE_MB: int = 500
    PREVIEW_DURATION_SECONDS: int = 30
    PREVIEW_FADE_DURATION: float = 0.5
    
    # Audio quality presets
    AUDIO_QUALITY_PRESETS: Dict[str, Dict[str, Any]] = {
        "high": {"bitrate": "320k", "sample_rate": 48000},
        "medium": {"bitrate": "192k", "sample_rate": 44100},
        "low": {"bitrate": "128k", "sample_rate": 44100},
        "preview": {"bitrate": "128k", "sample_rate": 44100}
    }
    
    # CORS settings
    CORS_ORIGINS: List[HttpUrl] = []
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    RATE_LIMIT_PER_HOUR: int = 1000
    UPLOAD_RATE_LIMIT_PER_DAY: int = 100
    
    # Email settings
    SMTP_HOST: str
    SMTP_PORT: int = 587
    SMTP_USER: str
    SMTP_PASSWORD: SecretStr
    SMTP_TLS: bool = True
    SMTP_SSL: bool = False
    EMAIL_FROM_NAME: str = "Music Store"
    EMAIL_FROM_ADDRESS: EmailStr
    
    # Frontend URL
    FRONTEND_URL: HttpUrl
    
    # Celery settings
    CELERY_BROKER_URL: Optional[RedisDsn] = None
    CELERY_RESULT_BACKEND: Optional[RedisDsn] = None
    CELERY_TASK_ALWAYS_EAGER: bool = False
    
    # Security settings
    SECRET_KEY: SecretStr  # For general encryption needs
    ALLOWED_HOSTS: List[str] = ["*"]
    SECURE_HEADERS_ENABLED: bool = True
    
    # Pagination
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # File upload settings
    UPLOAD_CHUNK_SIZE: int = 1024 * 1024  # 1MB chunks
    TEMP_UPLOAD_DIR: str = "/tmp/music-store-uploads"
    
    # Distribution settings
    DISTRIBUTION_PLATFORMS: List[str] = ["spotify", "apple_music", "youtube_music", "soundcloud"]
    DISTRIBUTION_CHECK_INTERVAL_HOURS: int = 6
    
    # Monitoring
    SENTRY_DSN: Optional[str] = None
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Feature flags
    ENABLE_DISTRIBUTION: bool = True
    ENABLE_ANALYTICS: bool = True
    ENABLE_SOCIAL_LOGIN: bool = False
    MAINTENANCE_MODE: bool = False
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | List[str]) -> List[str]:
        """Parse CORS origins from comma-separated string or list."""
        if isinstance(v, str) and v:
            return [origin.strip() for origin in v.split(",")]
        elif isinstance(v, list):
            return v
        return []
    
    @validator("CELERY_BROKER_URL", pre=True)
    def set_celery_broker(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Default Celery broker to Redis URL if not set."""
        if v is None and "REDIS_URL" in values:
            return values["REDIS_URL"]
        return v
    
    @validator("CELERY_RESULT_BACKEND", pre=True)
    def set_celery_backend(cls, v: Optional[str], values: Dict[str, Any]) -> str:
        """Default Celery backend to Redis URL if not set."""
        if v is None and "REDIS_URL" in values:
            return values["REDIS_URL"]
        return v
    
    @property
    def jwt_access_token_expire_timedelta(self) -> timedelta:
        """Get JWT access token expiration as timedelta."""
        return timedelta(minutes=self.JWT_ACCESS_TOKEN_EXPIRE_MINUTES)
    
    @property
    def jwt_refresh_token_expire_timedelta(self) -> timedelta:
        """Get JWT refresh token expiration as timedelta."""
        return timedelta(days=self.JWT_REFRESH_TOKEN_EXPIRE_DAYS)
    
    @property
    def jwt_email_verification_expire_timedelta(self) -> timedelta:
        """Get email verification token expiration as timedelta."""
        return timedelta(hours=self.JWT_EMAIL_VERIFICATION_EXPIRE_HOURS)
    
    @property
    def jwt_password_reset_expire_timedelta(self) -> timedelta:
        """Get password reset token expiration as timedelta."""
        return timedelta(hours=self.JWT_PASSWORD_RESET_EXPIRE_HOURS)
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
        
        # Custom environment variable names
        fields = {
            "DATABASE_URL": {"env": "DATABASE_URL"},
            "REDIS_URL": {"env": "REDIS_URL"},
            "B2_KEY_ID": {"env": "BACKBLAZE_KEY_ID"},
            "B2_APPLICATION_KEY": {"env": "BACKBLAZE_APPLICATION_KEY"},
        }


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.
    
    Returns:
        Settings: Application settings
    """
    return Settings()


# Create settings instance
settings = get_settings()
