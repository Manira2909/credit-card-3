from django.core.mail import send_mail
from django.conf import settings

def send_alert_email(to_email, subject, message):
    try:
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [to_email], fail_silently=False)
        print(f"✅ Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"❌ Email failed: {e}")
        return False

def check_and_notify(user, card, transaction_amount=None):
    if not user.email:
        user.email = "test@example.com"

    # 1. Transaction > 5000
    if transaction_amount and float(transaction_amount) > 5000:
        send_alert_email(user.email, "High Value Transaction Alert - Rs.{}".format(transaction_amount),
            f"Hi {user.username},\n\nAlert: Your card ending with {card.card_number[-4:]} was charged Rs.{transaction_amount} at {card.card_holder}.\nIf this wasn't you, please block your card immediately.\n\n- Credit Card Security Team")

    # 2. Card Blocked
    if card.is_blocked:
        send_alert_email(user.email, "Card Blocked Alert",
            f"Hi {user.username},\n\nYour card **** **** **** {card.card_number[-4:]} has been BLOCKED due to security reasons. Contact admin to unblock.\n\n- Security Team")

    # 3. Credit Limit < 10%
    available = float(card.credit_limit) - float(card.used_limit)
    limit_percent = (available / float(card.credit_limit)) * 100 if float(card.credit_limit) > 0 else 0
    if limit_percent < 10:
        send_alert_email(user.email, "Low Credit Limit Warning",
            f"Hi {user.username},\n\nWarning: Your available credit is only Rs.{available} ({limit_percent:.1f}%).\nTotal Limit: Rs.{card.credit_limit}\nUsed: Rs.{card.used_limit}\nPlease make payment soon.\n\n- Credit Card Team")