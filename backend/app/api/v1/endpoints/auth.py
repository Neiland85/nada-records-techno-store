"""
Authentication endpoints.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.security import create_access_token
from app.schemas.auth import Token, UserLogin
from app.api.deps import get_db

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
):
    # Implement login logic here
    # For now, return a dummy token
    access_token = create_access_token(data={"sub": "user@example.com"})
    return {"access_token": access_token, "token_type": "bearer"}
