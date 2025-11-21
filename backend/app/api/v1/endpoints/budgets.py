# Budget Management Endpoints
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.budget import Budget
from app.models.category import Category
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

router = APIRouter()

class BudgetCreate(BaseModel):
    category_id: Optional[int] = None
    amount: float
    period: str = "monthly"  # monthly, weekly, yearly
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    alert_threshold: float = 80.0  # Alert at 80% of budget

class BudgetUpdate(BaseModel):
    amount: Optional[float] = None
    period: Optional[str] = None
    alert_threshold: Optional[float] = None
    is_active: Optional[bool] = None

class BudgetResponse(BaseModel):
    id: int
    category_id: Optional[int]
    category_name: Optional[str]
    amount: float
    spent: float
    remaining: float
    percentage_used: float
    period: str
    is_active: bool
    alert_threshold: float
    created_at: datetime

@router.post("/", response_model=BudgetResponse)
async def create_budget(
    budget: BudgetCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new budget"""
    
    # Check if budget already exists for this category
    existing_budget = db.query(Budget).filter(
        and_(
            Budget.user_id == current_user.id,
            Budget.category_id == budget.category_id,
            Budget.is_active == True
        )
    ).first()
    
    if existing_budget:
        raise HTTPException(status_code=400, detail="Active budget already exists for this category")
    
    new_budget = Budget(
        user_id=current_user.id,
        category_id=budget.category_id,
        amount=budget.amount,
        period=budget.period,
        start_date=budget.start_date or datetime.now(),
        end_date=budget.end_date,
        alert_threshold=budget.alert_threshold,
        is_active=True
    )
    
    db.add(new_budget)
    db.commit()
    db.refresh(new_budget)
    
    # Calculate spent amount
    # TODO: Implement spent calculation from transactions
    
    category_name = None
    if budget.category_id:
        category = db.query(Category).filter(Category.id == budget.category_id).first()
        if category:
            category_name = category.name
    
    return BudgetResponse(
        id=new_budget.id,
        category_id=new_budget.category_id,
        category_name=category_name or "Overall",
        amount=new_budget.amount,
        spent=0.0,
        remaining=new_budget.amount,
        percentage_used=0.0,
        period=new_budget.period,
        is_active=new_budget.is_active,
        alert_threshold=new_budget.alert_threshold,
        created_at=new_budget.created_at
    )

@router.get("/", response_model=List[BudgetResponse])
async def get_budgets(
    active_only: bool = True,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get all budgets for the current user"""
    
    query = db.query(Budget).filter(Budget.user_id == current_user.id)
    
    if active_only:
        query = query.filter(Budget.is_active == True)
    
    budgets = query.all()
    
    result = []
    for budget in budgets:
        category_name = None
        if budget.category_id:
            category = db.query(Category).filter(Category.id == budget.category_id).first()
            if category:
                category_name = category.name
        
        # TODO: Calculate actual spent from transactions
        spent = 0.0
        remaining = budget.amount - spent
        percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0
        
        result.append(BudgetResponse(
            id=budget.id,
            category_id=budget.category_id,
            category_name=category_name or "Overall",
            amount=budget.amount,
            spent=spent,
            remaining=remaining,
            percentage_used=percentage_used,
            period=budget.period,
            is_active=budget.is_active,
            alert_threshold=budget.alert_threshold,
            created_at=budget.created_at
        ))
    
    return result

@router.get("/{budget_id}", response_model=BudgetResponse)
async def get_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific budget"""
    
    budget = db.query(Budget).filter(
        and_(
            Budget.id == budget_id,
            Budget.user_id == current_user.id
        )
    ).first()
    
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    category_name = None
    if budget.category_id:
        category = db.query(Category).filter(Category.id == budget.category_id).first()
        if category:
            category_name = category.name
    
    spent = 0.0  # TODO: Calculate from transactions
    remaining = budget.amount - spent
    percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0
    
    return BudgetResponse(
        id=budget.id,
        category_id=budget.category_id,
        category_name=category_name or "Overall",
        amount=budget.amount,
        spent=spent,
        remaining=remaining,
        percentage_used=percentage_used,
        period=budget.period,
        is_active=budget.is_active,
        alert_threshold=budget.alert_threshold,
        created_at=budget.created_at
    )

@router.put("/{budget_id}", response_model=BudgetResponse)
async def update_budget(
    budget_id: int,
    budget_update: BudgetUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update a budget"""
    
    budget = db.query(Budget).filter(
        and_(
            Budget.id == budget_id,
            Budget.user_id == current_user.id
        )
    ).first()
    
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    if budget_update.amount is not None:
        budget.amount = budget_update.amount
    if budget_update.period is not None:
        budget.period = budget_update.period
    if budget_update.alert_threshold is not None:
        budget.alert_threshold = budget_update.alert_threshold
    if budget_update.is_active is not None:
        budget.is_active = budget_update.is_active
    
    budget.updated_at = datetime.now()
    
    db.commit()
    db.refresh(budget)
    
    category_name = None
    if budget.category_id:
        category = db.query(Category).filter(Category.id == budget.category_id).first()
        if category:
            category_name = category.name
    
    spent = 0.0
    remaining = budget.amount - spent
    percentage_used = (spent / budget.amount * 100) if budget.amount > 0 else 0
    
    return BudgetResponse(
        id=budget.id,
        category_id=budget.category_id,
        category_name=category_name or "Overall",
        amount=budget.amount,
        spent=spent,
        remaining=remaining,
        percentage_used=percentage_used,
        period=budget.period,
        is_active=budget.is_active,
        alert_threshold=budget.alert_threshold,
        created_at=budget.created_at
    )

@router.delete("/{budget_id}")
async def delete_budget(
    budget_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a budget"""
    
    budget = db.query(Budget).filter(
        and_(
            Budget.id == budget_id,
            Budget.user_id == current_user.id
        )
    ).first()
    
    if not budget:
        raise HTTPException(status_code=404, detail="Budget not found")
    
    db.delete(budget)
    db.commit()
    
    return {"message": "Budget deleted successfully"}
