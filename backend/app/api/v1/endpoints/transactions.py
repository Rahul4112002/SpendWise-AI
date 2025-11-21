# Transactions endpoint
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from datetime import datetime

from app.database import SessionLocal
from app.models.transaction import Transaction
from app.models.user import User

router = APIRouter()

class TransactionCreate(BaseModel):
    amount: float
    description: str | None = None
    date: datetime

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=TransactionCreate)
def create_transaction(transaction: TransactionCreate, db: Session = Depends(get_db)):
    new_txn = Transaction(
        amount=transaction.amount,
        description=transaction.description,
        date=transaction.date,
        user_id=1  # Replace with actual user from auth session
    )
    db.add(new_txn)
    db.commit()
    db.refresh(new_txn)
    return new_txn

@router.get("/", response_model=List[TransactionCreate])
def get_transactions(db: Session = Depends(get_db)):
    return db.query(Transaction).filter(Transaction.user_id == 1).all()  # Replace with actual user logic
