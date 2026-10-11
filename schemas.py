from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime

class RegisterIn(BaseModel):
    email: str
    password: str

class LoginIn(BaseModel):
    email: str
    password: str

class CardIn(BaseModel):
    card_number: str
    holder_name: str
    expiry_month: int
    expiry_year: int
    cvv: str # validate only, not store ma!

class PayIn(BaseModel):
    card_id: int
    amount: float
    merchant: str = "Test Merchant"

# NEW - Dashboard ku use aagum
class TransactionOut(BaseModel):
    amount: float
    masked_card_number: str
    date: datetime
    status: str

    class Config:
        orm_mode = True # SQLAlchemy object ah direct ah convert panna

class DashboardSummary(BaseModel):
    total_transactions: int
    total_amount_spent: float
    current_month_spending: float
    available_credit_limit: float
    last_5_transactions: List[TransactionOut]