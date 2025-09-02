"""
Security utilities for authentication and password handling.
Provides JWT token creation/validation and password hashing.
"""
from datetime import datetime, timedelta
from typing import Optional, Union

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plain password against a hashed password.
    
    Args:
        plain_password: The plain text password
        hashed_password: The hashed password from database
        
    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password for storing in database.
    
    Args:
        password: The plain text password
        
    Returns:
        str: The hashed password
    """
    return pwd_context.hash(password)


def create_access_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT access token.
    
    Args:
        data: The payload data to encode in the token
        expires_delta: Token expiration time (optional)
        
    Returns:
        str: The encoded JWT token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.JWT_ACCESS_TOKEN_EXPIRE_MINUTES
        )
    
    to_encode.update({"exp": expire, "type": "access"})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY.get_secret_value(), 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_refresh_token(
    data: dict, 
    expires_delta: Optional[timedelta] = None
) -> str:
    """
    Create a JWT refresh token.
    
    Args:
        data: The payload data to encode in the token
        expires_delta: Token expiration time (optional)
        
    Returns:
        str: The encoded JWT refresh token
    """
    to_encode = data.copy()
    
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.JWT_REFRESH_TOKEN_EXPIRE_DAYS
        )
    
    to_encode.update({"exp": expire, "type": "refresh"})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY.get_secret_value(), 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_email_verification_token(email: str) -> str:
    """
    Create a JWT token for email verification.
    
    Args:
        email: The email address to verify
        
    Returns:
        str: The encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(
        hours=settings.JWT_EMAIL_VERIFICATION_EXPIRE_HOURS
    )
    
    to_encode = {
        "exp": expire,
        "email": email,
        "type": "email_verification"
    }
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY.get_secret_value(), 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def create_password_reset_token(email: str) -> str:
    """
    Create a JWT token for password reset.
    
    Args:
        email: The email address for password reset
        
    Returns:
        str: The encoded JWT token
    """
    expire = datetime.utcnow() + timedelta(
        hours=settings.JWT_PASSWORD_RESET_EXPIRE_HOURS
    )
    
    to_encode = {
        "exp": expire,
        "email": email,
        "type": "password_reset"
    }
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.JWT_SECRET_KEY.get_secret_value(), 
        algorithm=settings.JWT_ALGORITHM
    )
    
    return encoded_jwt


def verify_token(token: str, token_type: str) -> Optional[dict]:
    """
    Verify and decode a JWT token.
    
    Args:
        token: The JWT token to verify
        token_type: Expected token type (access, refresh, email_verification, password_reset)
        
    Returns:
        dict: The decoded token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, 
            settings.JWT_SECRET_KEY.get_secret_value(), 
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Verify token type
        if payload.get("type") != token_type:
            return None
            
        return payload
        
    except jwt.ExpiredSignatureError:
        return None
    except jwt.JWTError:
        return None
