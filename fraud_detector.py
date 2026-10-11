from django.utils import timezone
from datetime import timedelta
from.models import Transaction

def evaluate_fraud(user, card, amount, location, device_id):
    now = timezone.now()
    reasons = []
    is_fraud = False

    # Rule 1: Multiple high-value >5000 in 10 mins
    recent_high = Transaction.objects.filter(
        user=user, date__gte=now - timedelta(minutes=10), amount__gt=5000
    ).count()
    if recent_high >= 2 and float(amount) > 5000:
        reasons.append(f"{recent_high+1} high-value transactions in 10 mins")
        is_fraud = True

    # Rule 2: Rapid transactions diff locations/devices in 5 mins
    recent = Transaction.objects.filter(user=user, date__gte=now - timedelta(minutes=5))
    locations = set(r.location for r in recent)
    devices = set(r.device_id for r in recent)
    if len(locations) >= 2 or len(devices) >= 2:
        reasons.append(f"Rapid transactions from different locations {locations} / devices {devices}")
        is_fraud = True

    # Rule 3: Amount > 50% of credit limit single txn
    if float(amount) > float(card.credit_limit) * 0.5:
        reasons.append(f"Single transaction >50% of limit (Rs.{amount})")
        is_fraud = True

    status = 'FRAUD' if is_fraud else ('FLAGGED' if reasons else 'SAFE')
    return status, "; ".join(reasons)