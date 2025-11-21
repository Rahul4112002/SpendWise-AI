# Auth endpoint
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.core.security import (
    hash_password, 
    verify_password, 
    create_access_token,
    get_current_user
)
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta
from app.core.config import settings

router = APIRouter()

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str | None = None  # Accept 'name' from frontend
    full_name: str | None = None
    phone_number: str | None = None

class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str | None = None
    
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Use 'name' if provided, otherwise use 'full_name'
    full_name = user.name or user.full_name
    
    hashed_password = hash_password(user.password)
    new_user = User(
        email=user.email, 
        hashed_password=hashed_password,
        full_name=full_name,
        phone_number=user.phone_number
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token"""
    user = db.query(User).filter(User.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, 
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return current_user

