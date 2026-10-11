from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from . import models, database
from .auth import get_current_user
from .schemas import CardIn
from .security import luhn_check
import base64, os, uuid

router = APIRouter(prefix="/api/cards", tags=["Cards"])

def get_db():
    db = database.SessionLocal()
    try: yield db
    finally: db.close()

def encrypt_card(num: str) -> str:
    # Simple base64 for demo - final la AES use pannalam ma
    return base64.b64encode(num.encode()).decode()

@router.post("/")
def add_card(req: CardIn, curr = Depends(get_current_user), db: Session = Depends(get_db)):
    num = req.card_number.replace(" ", "")
    if not luhn_check(num): raise HTTPException(400, "Invalid card number")
    if len(req.cvv)!=3: raise HTTPException(400, "Invalid CVV")
    if req.expiry_year < 2025: raise HTTPException(400, "Card expired")
    
    # CVV save pannala ma! - rule follow
    card = models.CreditCard(
        user_id=curr.id,
        card_number_enc=encrypt_card(num),
        last_four=num[-4:],
        holder_name=req.holder_name,
        expiry_month=req.expiry_month,
        expiry_year=req.expiry_year,
        card_type="Visa" if num.startswith("4") else "MasterCard"
    )
    db.add(card); db.commit(); db.refresh(card)
    return {"msg": "Card added", "id": card.id, "last_four": card.last_four}

@router.get("/")
def my_cards(curr = Depends(get_current_user), db: Session = Depends(get_db)):
    cards = db.query(models.CreditCard).filter(models.CreditCard.user_id==curr.id).all()
    return [{"id": c.id, "last_four": c.last_four, "holder": c.holder_name, 
             "expiry": f"{c.expiry_month}/{c.expiry_year}", "type": c.card_type,
             "masked": f"**** **** **** {c.last_four}"} for c in cards]

@router.delete("/{card_id}")
def del_card(card_id: int, curr = Depends(get_current_user), db: Session = Depends(get_db)):
    c = db.query(models.CreditCard).filter(models.CreditCard.id==card_id, models.CreditCard.user_id==curr.id).first()
    if not c: raise HTTPException(404, "Not found")
    db.delete(c); db.commit()
    return {"msg": "Deleted ma!"}