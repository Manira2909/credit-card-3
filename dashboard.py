from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from.database import get_db
from. import models
from.security import get_current_user
from.schemas import DashboardSummary, TransactionOut
import datetime

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

def mask_card(last_four: str) -> str:
    """Card number ah mask panrathuku. Ex: **** 1234"""
    if not last_four:
        return "**** ****"
    return f"**** **** {last_four}"

@router.get("/summary", response_model=DashboardSummary)
def dashboard_summary(
    user_id: int = Depends(get_current_user), 
    db: Session = Depends(get_db)
):
    """
    Returns dashboard summary for logged in user
    Requires: JWT Token in Header
    """
    
    # 1. User iruka check pannu
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # 2. total_transactions - count of all transactions
    total_transactions = db.query(func.count(models.Transaction.id)).filter(
        models.Transaction.user_id == user_id
    ).scalar() or 0

    # 3. total_amount_spent - sum of all SUCCESS transactions - OPTIMIZED
    total_amount_spent = db.query(func.coalesce(func.sum(models.Transaction.amount), 0.0)).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.status == "success"
    ).scalar()

    # 4. current_month_spending - sum of this month SUCCESS transactions - OPTIMIZED
    now = datetime.datetime.utcnow()
    current_month_spending = db.query(func.coalesce(func.sum(models.Transaction.amount), 0.0)).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.status == "success",
        extract('year', models.Transaction.created_at) == now.year,
        extract('month', models.Transaction.created_at) == now.month
    ).scalar()

    # 5. available_credit_limit = User.balance - total_spent
    available_credit_limit = float(user.balance) - float(total_amount_spent)
    if available_credit_limit < 0:
        available_credit_limit = 0.0

    # 6. last_5_transactions - JOIN with credit_cards + LIMIT 5 - OPTIMIZED
    transactions_query = db.query(
        models.Transaction.amount,
        models.Transaction.status,
        models.Transaction.created_at,
        models.CreditCard.last_four
    ).join(
        models.CreditCard, models.Transaction.card_id == models.CreditCard.id
    ).filter(
        models.Transaction.user_id == user_id
    ).order_by(models.Transaction.created_at.desc()).limit(5).all()

    last_5_transactions = [
        TransactionOut(
            amount=float(t.amount),
            masked_card_number=mask_card(t.last_four),
            date=t.created_at,
            status=t.status
        ) for t in transactions_query
    ]

    return DashboardSummary(
        total_transactions=total_transactions,
        total_amount_spent=float(total_amount_spent),
        current_month_spending=float(current_month_spending),
        available_credit_limit=available_credit_limit,
        last_5_transactions=last_5_transactions
    )