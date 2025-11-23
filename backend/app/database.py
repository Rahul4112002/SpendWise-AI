# Database configuration - Supabase PostgreSQL
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Supabase-optimized connection parameters
connect_args = {}
if "supabase.co" in settings.DATABASE_URL:
    # Supabase-specific connection parameters
    connect_args = {
        "connect_timeout": 10,
        "options": "-c timezone=utc"
    }

# Create SQLAlchemy engine with Supabase optimization
engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    pool_recycle=3600,
    echo=settings.DEBUG,
    connect_args=connect_args
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

# Metadata
metadata = MetaData()

def get_db():
    """Dependency for getting database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
