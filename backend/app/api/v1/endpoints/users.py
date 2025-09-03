"""
User endpoints.
"""
from fastapi import APIRouter

router = APIRouter()

@router.get("/me")
async def get_current_user():
    # Implement get current user logic
    return {"user": {"id": 1, "email": "user@example.com"}}
