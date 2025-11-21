# AI Insight model for storing AI-generated recommendations
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class AIInsight(Base):
    __tablename__ = "ai_insights"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Insight details
    insight_type = Column(String, nullable=False)  # spending_alert, saving_tip, budget_recommendation, etc.
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    priority = Column(String, default="medium")  # low, medium, high, urgent
    
    # Context
    category = Column(String, nullable=True)
    related_amount = Column(String, nullable=True)
    
    # Status
    is_read = Column(Boolean, default=False)
    is_actionable = Column(Boolean, default=False)
    action_taken = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="ai_insights")
