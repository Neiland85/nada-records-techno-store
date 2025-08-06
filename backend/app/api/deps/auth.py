"""
JWT authentication dependencies and utilities.
"""
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Union

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.config import settings
from app.models import User, UserSession
from app.models.base import AsyncSessionLocal


# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=True,
)


class AuthService:
    """Authentication service for JWT operations."""
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Generate password hash."""
        return pwd_context.hash(password)
    
    @staticmethod
    def create_access_token(
        subject: Union[str, Any],
        expires_delta: Optional[timedelta] = None,
        additional_claims: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Create JWT access token.
        
        Args:
            subject: Token subject (usually user ID)
            expires_delta: Token expiration time
            additional_claims: Additional JWT claims
            
        Returns:
            Encoded JWT token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + settings.jwt_access_token_expire_timedelta
        
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "access",
            "iat": datetime.utcnow(),
        }
        
        if additional_claims:
            to_encode.update(additional_claims)
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt
    
    @staticmethod
    def create_refresh_token(
        subject: Union[str, Any],
        expires_delta: Optional[timedelta] = None,
    ) -> str:
        """
        Create JWT refresh token.
        
        Args:
            subject: Token subject (usually user ID)
            expires_delta: Token expiration time
            
        Returns:
            Encoded JWT refresh token
        """
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + settings.jwt_refresh_token_expire_timedelta
        
        to_encode = {
            "exp": expire,
            "sub": str(subject),
            "type": "refresh",
            "iat": datetime.utcnow(),
        }
        
        encoded_jwt = jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT_ALGORITHM,
        )
        return encoded_jwt
    
    @staticmethod
    def create_email_verification_token(email: str) -> str:
        """Create email verification token."""
        expire = datetime.utcnow() + settings.jwt_email_verification_expire_timedelta
        to_encode = {
            "exp": expire,
            "sub": email,
            "type": "email_verification",
        }
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT_ALGORITHM,
        )
    
    @staticmethod
    def create_password_reset_token(email: str) -> str:
        """Create password reset token."""
        expire = datetime.utcnow() + settings.jwt_password_reset_expire_timedelta
        to_encode = {
            "exp": expire,
            "sub": email,
            "type": "password_reset",
        }
        return jwt.encode(
            to_encode,
            settings.JWT_SECRET_KEY.get_secret_value(),
            algorithm=settings.JWT_ALGORITHM,
        )
    
    @staticmethod
    def decode_token(token: str) -> Dict[str, Any]:
        """
        Decode and validate JWT token.
        
        Args:
            token: JWT token to decode
            
        Returns:
            Token payload
            
        Raises:
            HTTPException: If token is invalid
        """
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY.get_secret_value(),
                algorithms=[settings.JWT_ALGORITHM],
            )
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )


# Dependency functions
async def get_db() -> AsyncSession:
    """Get database session."""
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """
    Get current authenticated user.
    
    Args:
        db: Database session
        token: JWT access token
        
    Returns:
        Current user object
        
    Raises:
        HTTPException: If authentication fails
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = AuthService.decode_token(token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise credentials_exception
            
    except (JWTError, ValidationError):
        raise credentials_exception
    
    # Get user from database
    result = await db.execute(
        select(User).where(User.id == user_id)
    )
    user = result.scalar_one_or_none()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    
    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """
    Get current active user.
    
    Args:
        current_user: Current user from JWT
        
    Returns:
        Active user object
        
    Raises:
        HTTPException: If user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get current verified user.
    
    Args:
        current_user: Current active user
        
    Returns:
        Verified user object
        
    Raises:
        HTTPException: If user is not verified
    """
    if not current_user.is_verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email not verified",
        )
    return current_user


async def get_current_admin_user(
    current_user: User = Depends(get_current_active_user),
) -> User:
    """
    Get current admin user.
    
    Args:
        current_user: Current active user
        
    Returns:
        Admin user object
        
    Raises:
        HTTPException: If user is not admin
    """
    if not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions",
        )
    return current_user


async def get_current_artist_user(
    current_user: User = Depends(get_current_verified_user),
) -> User:
    """
    Get current artist user.
    
    Args:
        current_user: Current verified user
        
    Returns:
        Artist user object
        
    Raises:
        HTTPException: If user is not an artist
    """
    if not current_user.is_artist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Artist account required",
        )
    return current_user


class RoleChecker:
    """
    Role-based access control dependency.
    
    Usage:
        @router.get("/admin", dependencies=[Depends(RoleChecker(["admin"]))])
    """
    
    def __init__(self, allowed_roles: list[str]):
        self.allowed_roles = allowed_roles
    
    async def __call__(self, user: User = Depends(get_current_active_user)):
        if user.role not in self.allowed_roles and not user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Operation not permitted",
            )


class PermissionChecker:
    """
    Permission-based access control dependency.
    
    Usage:
        @router.post("/upload", dependencies=[Depends(PermissionChecker("upload_music"))])
    """
    
    def __init__(self, required_permission: str):
        self.required_permission = required_permission
    
    async def __call__(self, user: User = Depends(get_current_active_user)):
        if not user.has_permission(self.required_permission):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Permission '{self.required_permission}' required",
            )


# Rate limiting decorator
from functools import wraps
from typing import Callable
import asyncio
from collections import defaultdict
from datetime import datetime


class RateLimiter:
    """Simple in-memory rate limiter."""
    
    def __init__(self):
        self.requests = defaultdict(list)
    
    def is_allowed(self, key: str, max_requests: int, window_seconds: int) -> bool:
        """Check if request is allowed within rate limit."""
        now = datetime.utcnow()
        minute_ago = now - timedelta(seconds=window_seconds)
        
        # Clean old requests
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if req_time > minute_ago
        ]
        
        # Check rate limit
        if len(self.requests[key]) >= max_requests:
            return False
        
        # Add current request
        self.requests[key].append(now)
        return True


rate_limiter = RateLimiter()


def rate_limit(max_requests: int = 60, window_seconds: int = 60):
    """
    Rate limiting decorator.
    
    Args:
        max_requests: Maximum requests allowed
        window_seconds: Time window in seconds
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Get user from kwargs
            user = kwargs.get("current_user") or kwargs.get("user")
            if user:
                key = f"user:{user.id}"
            else:
                # Fall back to IP-based rate limiting
                request = kwargs.get("request")
                key = f"ip:{request.client.host}" if request else "anonymous"
            
            if not rate_limiter.is_allowed(key, max_requests, window_seconds):
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Rate limit exceeded",
                )
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator