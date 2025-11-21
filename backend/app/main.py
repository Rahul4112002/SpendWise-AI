# Main application entry point
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.core.config import settings
from app.api.v1.endpoints import auth, transactions, bank_statements, users, analytics, ai, budgets, categories
import os

# Import all models to ensure they are registered with SQLAlchemy
from app.models import user, transaction, bank_statement, category, budget, ai_insight, spending_pattern

# Create database tables
Base.metadata.create_all(bind=engine)

# Create upload directory
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Autonomous Financial Coaching Agent for Gig Workers and Everyday Citizens - Built for InTech Problem Statement 1"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(transactions.router, prefix="/api/v1/transactions", tags=["Transactions"])
app.include_router(bank_statements.router, prefix="/api/v1/bank-statements", tags=["Bank Statements"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users"])
app.include_router(analytics.router, prefix="/api/v1/analytics", tags=["Analytics"])
app.include_router(ai.router, prefix="/api/v1/ai", tags=["AI Coach"])
app.include_router(budgets.router, prefix="/api/v1/budgets", tags=["Budgets"])
app.include_router(categories.router, prefix="/api/v1/categories", tags=["Categories"])

@app.get("/")
async def root():
    return {
        "message": "Welcome to PennyWise AI - Autonomous Financial Coach",
        "version": settings.VERSION,
        "description": "Built for InTech Problem Statement 1 - Autonomous financial coaching for gig workers and everyday citizens",
        "docs": "/docs",
        "features": [
            "SMS-powered transaction tracking",
            "Bank statement PDF parsing",
            "AI-powered spending analysis",
            "Anomaly detection",
            "Subscription identification",
            "Proactive budget recommendations",
            "Interactive AI chat",
            "Adaptive to income variability"
        ]
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",
        "ai_service": "ready" if settings.GROQ_API_KEY else "not_configured"
    }
