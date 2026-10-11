from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database
from .auth import get_current_user
from .schemas import PayIn
import uuid

router = APIRouter(prefix="/api/payments", tags=["Payments"])

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

@router.post("/pay")
def pay(req: PayIn, curr = Depends(get_current_user), db: Session = Depends(get_db)):
    card = db.query(models.CreditCard).filter(models.CreditCard.id==req.card_id, models.CreditCard.user_id==curr.id).first()
    if not card: raise HTTPException(404, "Card not found")
    if curr.balance < req.amount: raise HTTPException(400, "Insufficient balance")
    
    curr.balance -= req.amount
    txn = models.Transaction(
        user_id=curr.id, card_id=card.id, amount=req.amount,
        merchant=req.merchant, status="success", txn_id=str(uuid.uuid4())[:8].upper()
    )
    db.add(txn); db.commit(); db.refresh(txn)
    return {"msg": "Payment success ma!", "txn_id": txn.txn_id, "balance": curr.balance}

@router.get("/")
def history(curr = Depends(get_current_user), db: Session = Depends(get_db)):
    txns = db.query(models.Transaction).filter(models.Transaction.user_id==curr.id).order_by(models.Transaction.created_at.desc()).all()
    return txns