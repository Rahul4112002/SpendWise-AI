# Transaction model
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Transaction details
    amount = Column(Float, nullable=False)
    transaction_type = Column(String, nullable=False)  # debit, credit
    category = Column(String, default="uncategorized")  # food, transport, bills, etc.
    merchant_name = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    
    # Date information
    transaction_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # SMS Metadata
    from_sms = Column(Boolean, default=False)
    sms_sender = Column(String, nullable=True)
    raw_sms_text = Column(Text, nullable=True)
    
    # Bank information
    bank_name = Column(String, nullable=True)
    account_last4 = Column(String, nullable=True)
    
    # Subscription detection
    is_recurring = Column(Boolean, default=False)
    recurring_pattern = Column(String, nullable=True)  # monthly, weekly, yearly
    
    # AI categorization confidence
    category_confidence = Column(Float, default=0.0)
    
    # Relationships
    user = relationship("User", back_populates="transactions")
