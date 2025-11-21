# Users endpoint
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter()

@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """Get current user profile"""
    return {
        "id": current_user.id,
        "email": current_user.email,
        "full_name": current_user.full_name,
        "user_type": current_user.user_type
    }

@router.put("/profile")
async def update_profile(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update user profile"""
    # TODO: Implement profile update
    return {"message": "Profile update endpoint - implementation pending"}

