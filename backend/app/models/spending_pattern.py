# Spending Pattern model for analyzing user behavior
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class SpendingPattern(Base):
    __tablename__ = "spending_patterns"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Pattern details
    pattern_type = Column(String, nullable=False)  # recurring, seasonal, anomaly, trend
    category = Column(String, nullable=True)
    description = Column(Text, nullable=False)
    
    # Financial metrics
    average_amount = Column(Float, default=0.0)
    frequency = Column(String, nullable=True)  # daily, weekly, monthly
    confidence_score = Column(Float, default=0.0)
    
    # Time period
    detected_at = Column(DateTime, default=datetime.utcnow)
    period_start = Column(DateTime, nullable=True)
    period_end = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User")
