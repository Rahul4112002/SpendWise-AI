# Category model for transaction categorization
from sqlalchemy import Column, Integer, String, Text, Boolean
from app.database import Base

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False, index=True)
    display_name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    icon = Column(String, nullable=True)
    color = Column(String, nullable=True)
    parent_category = Column(String, nullable=True)
    keywords = Column(Text, nullable=True)  # Comma-separated keywords for matching
    is_active = Column(Boolean, default=True)
    
    # Category types: expense, income
    category_type = Column(String, default="expense")
