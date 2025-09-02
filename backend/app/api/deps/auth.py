"""
Authentication dependencies.
Provides JWT token validation and user authentication for API endpoints.
"""
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.models.user import User
from app.api.deps.database import get_db

# OAuth2 scheme for token extraction
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    auto_error=False
)


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> Optional[User]:
    """
    Get current user from JWT token (optional - returns None if no valid token).
    Useful for endpoints that work for both authenticated and anonymous users.
    """
    if not token:
        return None
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY.get_secret_value(), 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            return None
    except JWTError:
        return None
    
    # TODO: Get user from database by ID
    # user = await get_user_by_id(db, user_id=user_id)
    # return user
    
    # Placeholder return
    return None


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """
    Get current user from JWT token (required).
    Raises HTTPException if token is invalid or user not found.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    if not token:
        raise credentials_exception
    
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY.get_secret_value(), 
            algorithms=[settings.JWT_ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # TODO: Get user from database by ID
    # user = await get_user_by_id(db, user_id=user_id)
    # if user is None:
    #     raise credentials_exception
    # return user
    
    # Placeholder - raise not implemented for now
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User authentication not yet implemented"
    )


async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """
    Get current active user (not disabled).
    """
    # TODO: Check if user is active/not disabled
    # if not current_user.is_active:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST, 
    #         detail="Inactive user"
    #     )
    
    return current_user


async def get_current_verified_user(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current verified user (email verified).
    """
    # TODO: Check if user email is verified
    # if not current_user.is_verified:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Email not verified"
    #     )
    
    return current_user


async def get_current_artist(
    current_user: User = Depends(get_current_active_user)
) -> User:
    """
    Get current user with artist profile.
    Ensures the user has an active artist profile.
    """
    # TODO: Check if user has artist profile
    # if not current_user.artist_profile:
    #     raise HTTPException(
    #         status_code=status.HTTP_400_BAD_REQUEST,
    #         detail="Artist profile required"
    #     )
    
    return current_user