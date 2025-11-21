# Categories Management Endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.category import Category
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

router = APIRouter()

class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    icon: Optional[str] = None
    color: Optional[str] = None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    icon: Optional[str]
    color: Optional[str]
    created_at: datetime

@router.get("/", response_model=List[CategoryResponse])
async def get_categories(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all categories"""
    
    categories = db.query(Category).all()
    
    return [
        CategoryResponse(
            id=c.id,
            name=c.name,
            description=c.description,
            icon=c.icon,
            color=c.color,
            created_at=c.created_at
        )
        for c in categories
    ]

@router.post("/", response_model=CategoryResponse)
async def create_category(
    category: CategoryCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new category"""
    
    # Check if category with same name exists
    existing = db.query(Category).filter(Category.name == category.name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category with this name already exists")
    
    new_category = Category(
        name=category.name,
        description=category.description,
        icon=category.icon,
        color=category.color
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return CategoryResponse(
        id=new_category.id,
        name=new_category.name,
        description=new_category.description,
        icon=new_category.icon,
        color=new_category.color,
        created_at=new_category.created_at
    )

@router.get("/{category_id}", response_model=CategoryResponse)
async def get_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific category"""
    
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        icon=category.icon,
        color=category.color,
        created_at=category.created_at
    )

@router.put("/{category_id}", response_model=CategoryResponse)
async def update_category(
    category_id: int,
    category_update: CategoryUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a category"""
    
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if category_update.name is not None:
        category.name = category_update.name
    if category_update.description is not None:
        category.description = category_update.description
    if category_update.icon is not None:
        category.icon = category_update.icon
    if category_update.color is not None:
        category.color = category_update.color
    
    db.commit()
    db.refresh(category)
    
    return CategoryResponse(
        id=category.id,
        name=category.name,
        description=category.description,
        icon=category.icon,
        color=category.color,
        created_at=category.created_at
    )

@router.delete("/{category_id}")
async def delete_category(
    category_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a category"""
    
    category = db.query(Category).filter(Category.id == category_id).first()
    
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db.delete(category)
    db.commit()
    
    return {"message": "Category deleted successfully"}

@router.post("/init-default")
async def initialize_default_categories(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Initialize default categories"""
    
    default_categories = [
        {"name": "Food & Dining", "icon": "🍔", "color": "#FF6B6B"},
        {"name": "Transport", "icon": "🚗", "color": "#4ECDC4"},
        {"name": "Shopping", "icon": "🛍️", "color": "#45B7D1"},
        {"name": "Bills & Utilities", "icon": "💡", "color": "#FFA07A"},
        {"name": "Entertainment", "icon": "🎬", "color": "#DDA15E"},
        {"name": "Healthcare", "icon": "🏥", "color": "#BC6C25"},
        {"name": "Education", "icon": "📚", "color": "#606C38"},
        {"name": "Groceries", "icon": "🛒", "color": "#283618"},
        {"name": "Income", "icon": "💰", "color": "#52B788"},
        {"name": "Transfer", "icon": "↔️", "color": "#95D5B2"},
    ]
    
    created_count = 0
    for cat_data in default_categories:
        existing = db.query(Category).filter(Category.name == cat_data["name"]).first()
        if not existing:
            category = Category(**cat_data)
            db.add(category)
            created_count += 1
    
    db.commit()
    
    return {"message": f"Initialized {created_count} default categories"}
