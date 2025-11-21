# Bank statements endpoint
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models.user import User
from app.core.security import get_current_user

router = APIRouter()

@router.post("/upload")
async def upload_statement(
    file: UploadFile = File(...),
    password: Optional[str] = Form(None),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Upload a bank statement PDF"""
    # TODO: Implement PDF processing
    return {
        "message": "Bank statement upload endpoint - implementation pending",
        "filename": file.filename
    }

@router.get("/")
async def get_statements(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all bank statements for current user"""
    # TODO: Implement statement retrieval
    return {"message": "Get statements endpoint - implementation pending"}

