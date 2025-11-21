# AI Coach Endpoints - Autonomous Financial Coaching
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from sqlalchemy import and_
from app.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.transaction import Transaction
from app.models.ai_insight import AIInsight
from app.models.spending_pattern import SpendingPattern
from app.services.ai_coach import AutonomousFinancialCoach
from typing import List, Optional
from datetime import datetime, timedelta
from pydantic import BaseModel

router = APIRouter()

class ChatMessage(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime

class InsightResponse(BaseModel):
    id: int
    title: str
    description: str
    insight_type: str
    priority: str
    created_at: datetime

class SpendingAnalysisRequest(BaseModel):
    days: int = 30

class SpendingAnalysisResponse(BaseModel):
    analysis: str
    metrics: dict
    recommendations: List[str]

@router.post("/chat", response_model=ChatResponse)
async def chat_with_ai(
    message: ChatMessage,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Interactive chat with AI financial coach"""
    
    try:
        coach = AutonomousFinancialCoach()
        
        # Get user's recent transactions for context
        recent_transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.created_at >= datetime.now() - timedelta(days=30)
            )
        ).all()
        
        # Prepare user context
        user_context = {
            "user_type": current_user.user_type,
            "average_income": current_user.average_monthly_income,
            "income_variability": current_user.income_variability,
            "currency": current_user.preferred_currency
        }
        
        # Get conversation history (last 10 messages)
        # TODO: Implement conversation history storage
        conversation_history = []
        
        response = await coach.chat_with_user(
            message.message,
            conversation_history,
            user_context
        )
        
        return ChatResponse(
            response=response,
            timestamp=datetime.now()
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI chat error: {str(e)}")

@router.post("/analyze-spending", response_model=SpendingAnalysisResponse)
async def analyze_spending(
    request: SpendingAnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-powered spending analysis and recommendations"""
    
    try:
        coach = AutonomousFinancialCoach()
        
        # Get transactions for the period
        start_date = datetime.now() - timedelta(days=request.days)
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.created_at >= start_date
            )
        ).all()
        
        # Convert to dict format
        transaction_dicts = [
            {
                "amount": t.amount,
                "transaction_type": t.transaction_type,
                "category": t.category_id,
                "merchant_name": t.merchant_name,
                "date": t.created_at.isoformat()
            }
            for t in transactions
        ]
        
        # User profile
        user_profile = {
            "user_type": current_user.user_type,
            "average_monthly_income": current_user.average_monthly_income,
            "income_variability": current_user.income_variability
        }
        
        # Get analysis
        analysis_result = await coach.analyze_spending_patterns(
            transaction_dicts,
            user_profile
        )
        
        # Save insights to database
        background_tasks.add_task(
            save_insights,
            db,
            current_user.id,
            analysis_result
        )
        
        return SpendingAnalysisResponse(
            analysis=analysis_result["analysis"],
            metrics=analysis_result["metrics"],
            recommendations=extract_recommendations(analysis_result["analysis"])
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis error: {str(e)}")

@router.get("/insights", response_model=List[InsightResponse])
async def get_ai_insights(
    days: int = 30,
    insight_type: Optional[str] = None,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated insights and recommendations"""
    
    start_date = datetime.now() - timedelta(days=days)
    
    query = db.query(AIInsight).filter(
        and_(
            AIInsight.user_id == current_user.id,
            AIInsight.created_at >= start_date
        )
    )
    
    if insight_type:
        query = query.filter(AIInsight.insight_type == insight_type)
    
    insights = query.order_by(AIInsight.created_at.desc()).all()
    
    return [
        InsightResponse(
            id=i.id,
            title=i.title,
            description=i.description,
            insight_type=i.insight_type,
            priority=i.priority,
            created_at=i.created_at
        )
        for i in insights
    ]

@router.post("/detect-anomalies")
async def detect_spending_anomalies(
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Detect unusual spending patterns and anomalies"""
    
    try:
        coach = AutonomousFinancialCoach()
        
        # Get last 60 days of transactions
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.transaction_type == "debit",
                Transaction.created_at >= datetime.now() - timedelta(days=60)
            )
        ).all()
        
        # Analyze for anomalies
        anomalies = await coach.detect_anomalies(
            [{"amount": t.amount, "merchant_name": t.merchant_name, "category": t.category_id, "date": t.created_at} for t in transactions]
        )
        
        # Save anomaly insights
        for anomaly in anomalies:
            insight = AIInsight(
                user_id=current_user.id,
                title=f"Unusual Spending Detected: {anomaly['category']}",
                description=anomaly["description"],
                insight_type="anomaly",
                priority="high" if anomaly["severity"] > 2 else "medium",
                metadata=anomaly
            )
            db.add(insight)
        
        db.commit()
        
        return {"anomalies": anomalies, "count": len(anomalies)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Anomaly detection error: {str(e)}")

@router.get("/subscriptions")
async def identify_subscriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Identify recurring payments and subscriptions"""
    
    try:
        coach = AutonomousFinancialCoach()
        
        # Get last 90 days for pattern detection
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.transaction_type == "debit",
                Transaction.created_at >= datetime.now() - timedelta(days=90)
            )
        ).all()
        
        transaction_dicts = [
            {
                "amount": t.amount,
                "merchant_name": t.merchant_name,
                "category": t.category_id,
                "date": t.created_at
            }
            for t in transactions
        ]
        
        subscriptions = await coach.identify_subscriptions(transaction_dicts)
        
        return {"subscriptions": subscriptions, "count": len(subscriptions)}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Subscription detection error: {str(e)}")

@router.get("/spending-patterns")
async def get_spending_patterns(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get detected spending patterns"""
    
    patterns = db.query(SpendingPattern).filter(
        SpendingPattern.user_id == current_user.id
    ).order_by(SpendingPattern.created_at.desc()).limit(10).all()
    
    return [
        {
            "id": p.id,
            "pattern_type": p.pattern_type,
            "description": p.description,
            "frequency": p.frequency,
            "average_amount": p.average_amount,
            "created_at": p.created_at
        }
        for p in patterns
    ]

@router.post("/generate-budget")
async def generate_ai_budget(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate AI-powered budget recommendations"""
    
    try:
        coach = AutonomousFinancialCoach()
        
        # Get income and spending history
        transactions = db.query(Transaction).filter(
            and_(
                Transaction.user_id == current_user.id,
                Transaction.created_at >= datetime.now() - timedelta(days=60)
            )
        ).all()
        
        # Calculate income statistics
        income_transactions = [t for t in transactions if t.transaction_type == "credit"]
        avg_income = sum(t.amount for t in income_transactions) / 2 if income_transactions else 0  # 2 months
        
        # Get spending by category
        category_spending = {}
        for t in transactions:
            if t.transaction_type == "debit":
                cat = t.category_id or "uncategorized"
                category_spending[cat] = category_spending.get(cat, 0) + t.amount
        
        # Generate recommendations
        budget_recommendations = await coach.generate_budget_recommendations(
            avg_income,
            category_spending,
            {
                "user_type": current_user.user_type,
                "income_variability": current_user.income_variability
            }
        )
        
        return budget_recommendations
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Budget generation error: {str(e)}")

# Helper functions
def save_insights(db: Session, user_id: int, analysis_result: dict):
    """Save analysis insights to database"""
    try:
        insight = AIInsight(
            user_id=user_id,
            title="Spending Analysis",
            description=analysis_result["analysis"][:500],
            insight_type="analysis",
            priority="medium",
            metadata=analysis_result["metrics"]
        )
        db.add(insight)
        db.commit()
    except Exception as e:
        print(f"Error saving insights: {e}")

def extract_recommendations(analysis: str) -> List[str]:
    """Extract recommendations from AI analysis"""
    # Simple extraction - look for bullet points or numbered items
    recommendations = []
    lines = analysis.split("\n")
    for line in lines:
        line = line.strip()
        if line.startswith(("-", "•", "*")) or (len(line) > 0 and line[0].isdigit() and ". " in line):
            recommendations.append(line.lstrip("-•* ").lstrip("0123456789. "))
    return recommendations[:5]  # Top 5 recommendations
