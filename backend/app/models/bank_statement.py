# Bank statement model
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class BankStatement(Base):
    __tablename__ = "bank_statements"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # File information
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_size = Column(Integer, nullable=False)
    
    # Bank details
    bank_name = Column(String, nullable=True)
    account_number = Column(String, nullable=True)
    statement_period_start = Column(DateTime, nullable=True)
    statement_period_end = Column(DateTime, nullable=True)
    
    # Processing status
    is_processed = Column(Boolean, default=False)
    is_encrypted = Column(Boolean, default=False)
    processing_status = Column(String, default="pending")  # pending, processing, completed, failed
    error_message = Column(Text, nullable=True)
    
    # Extracted data
    total_transactions = Column(Integer, default=0)
    extracted_text = Column(Text, nullable=True)
    
    # Timestamps
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    processed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="bank_statements")
