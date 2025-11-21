# Analytics Endpoints - Spending Analysis & Insights
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, extract
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.models.category import Category
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter()

class SpendingByCategory(BaseModel):
    category: str
    total: float
    transaction_count: int
    percentage: float

class MonthlyTrend(BaseModel):
    month: str
    income: float
    expenses: float
    savings: float

class AnalyticsSummary(BaseModel):
    total_income: float
    total_expenses: float
    net_savings: float
    savings_rate: float
    top_categories: List[SpendingByCategory]
    monthly_trends: List[MonthlyTrend]
    average_transaction: float
    transaction_count: int

@router.get("/summary", response_model=AnalyticsSummary)
async def get_analytics_summary(
    days: int = Query(30, description="Number of days to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get comprehensive analytics summary for the specified period"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    # Get transactions for the period
    transactions = db.query(Transaction).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.created_at >= start_date
        )
    ).all()
    
    # Calculate totals
    total_income = sum(t.amount for t in transactions if t.transaction_type == "credit")
    total_expenses = sum(t.amount for t in transactions if t.transaction_type == "debit")
    net_savings = total_income - total_expenses
    savings_rate = (net_savings / total_income * 100) if total_income > 0 else 0
    
    # Category-wise spending
    category_spending = {}
    for t in transactions:
        if t.transaction_type == "debit":
            cat = t.category_id or "uncategorized"
            if cat not in category_spending:
                category_spending[cat] = {"total": 0, "count": 0}
            category_spending[cat]["total"] += t.amount
            category_spending[cat]["count"] += 1
    
    # Format top categories
    top_categories = []
    for cat, data in sorted(category_spending.items(), key=lambda x: x[1]["total"], reverse=True)[:5]:
        category_name = cat
        if cat != "uncategorized":
            cat_obj = db.query(Category).filter(Category.id == cat).first()
            if cat_obj:
                category_name = cat_obj.name
        
        top_categories.append(SpendingByCategory(
            category=category_name,
            total=data["total"],
            transaction_count=data["count"],
            percentage=(data["total"] / total_expenses * 100) if total_expenses > 0 else 0
        ))
    
    # Monthly trends (last 6 months)
    monthly_trends = []
    for i in range(6):
        month_start = datetime.now() - timedelta(days=30 * (5 - i))
        month_end = month_start + timedelta(days=30)
        
        month_transactions = [t for t in transactions if month_start <= t.created_at < month_end]
        month_income = sum(t.amount for t in month_transactions if t.transaction_type == "credit")
        month_expenses = sum(t.amount for t in month_transactions if t.transaction_type == "debit")
        
        monthly_trends.append(MonthlyTrend(
            month=month_start.strftime("%b %Y"),
            income=month_income,
            expenses=month_expenses,
            savings=month_income - month_expenses
        ))
    
    return AnalyticsSummary(
        total_income=total_income,
        total_expenses=total_expenses,
        net_savings=net_savings,
        savings_rate=savings_rate,
        top_categories=top_categories,
        monthly_trends=monthly_trends,
        average_transaction=(total_expenses / len([t for t in transactions if t.transaction_type == "debit"])) if transactions else 0,
        transaction_count=len(transactions)
    )

@router.get("/spending-by-category")
async def get_spending_by_category(
    days: int = Query(30),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detailed spending breakdown by category"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    transactions = db.query(Transaction).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "debit",
            Transaction.created_at >= start_date
        )
    ).all()
    
    category_data = {}
    for t in transactions:
        cat = t.category_id or "uncategorized"
        if cat not in category_data:
            category_data[cat] = {
                "transactions": [],
                "total": 0,
                "avg": 0,
                "max": 0,
                "min": float('inf')
            }
        
        category_data[cat]["transactions"].append(t.amount)
        category_data[cat]["total"] += t.amount
        category_data[cat]["max"] = max(category_data[cat]["max"], t.amount)
        category_data[cat]["min"] = min(category_data[cat]["min"], t.amount)
    
    # Calculate averages
    for cat in category_data:
        category_data[cat]["avg"] = category_data[cat]["total"] / len(category_data[cat]["transactions"])
        category_data[cat]["count"] = len(category_data[cat]["transactions"])
        del category_data[cat]["transactions"]
    
    return category_data

@router.get("/income-vs-expenses")
async def get_income_vs_expenses(
    months: int = Query(6, description="Number of months to analyze"),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get monthly income vs expenses comparison"""
    
    data = []
    
    for i in range(months):
        month_date = datetime.now() - timedelta(days=30 * i)
        month_start = month_date.replace(day=1)
        next_month = (month_start + timedelta(days=32)).replace(day=1)
        
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.created_at >= month_start,
                Transaction.created_at < next_month
            )
        ).all()
        
        income = sum(t.amount for t in transactions if t.transaction_type == "credit")
        expenses = sum(t.amount for t in transactions if t.transaction_type == "debit")
        
        data.insert(0, {
            "month": month_start.strftime("%b %Y"),
            "income": income,
            "expenses": expenses,
            "savings": income - expenses
        })
    
    return data

@router.get("/top-merchants")
async def get_top_merchants(
    days: int = Query(30),
    limit: int = Query(10),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get top merchants by spending"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    merchant_spending = db.query(
        Transaction.merchant_name,
        func.sum(Transaction.amount).label("total"),
        func.count(Transaction.id).label("count")
    ).filter(
        and_(
            Transaction.user_id == current_user.id,
            Transaction.transaction_type == "debit",
            Transaction.created_at >= start_date,
            Transaction.merchant_name.isnot(None)
        )
    ).group_by(Transaction.merchant_name).order_by(
        func.sum(Transaction.amount).desc()
    ).limit(limit).all()
    
    return [
        {
            "merchant": m[0],
            "total_spent": float(m[1]),
            "transaction_count": m[2]
        }
        for m in merchant_spending
    ]

@router.get("/daily-spending")
async def get_daily_spending(
    days: int = Query(30),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get daily spending trend"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    daily_data = []
    for i in range(days):
        day = start_date + timedelta(days=i)
        day_end = day + timedelta(days=1)
        
        day_transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.transaction_type == "debit",
                Transaction.created_at >= day,
                Transaction.created_at < day_end
            )
        ).all()
        
        total = sum(t.amount for t in day_transactions)
        
        daily_data.append({
            "date": day.strftime("%Y-%m-%d"),
            "amount": total,
            "count": len(day_transactions)
        })
    
    return daily_data
