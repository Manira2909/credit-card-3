from django.core.mail import send_mail
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from.models import Card, Transaction

@receiver(post_save, sender=Transaction)
def check_transaction_alerts(sender, instance, created, **kwargs):
    if not created: return
    user_email = instance.user.email

    # 1. Amount > 5000
    if instance.amount > 5000:
        send_mail(
            'High Value Transaction Alert',
            f'Your transaction of Rs.{instance.amount} on card {instance.card.masked_number} is successful.',
            settings.EMAIL_HOST_USER,
            [user_email]
        )
    # 2. Credit limit < 10%
    card = instance.card
    remaining = card.credit_limit - card.used_limit
    if remaining < (card.credit_limit * 0.1):
        send_mail(
            'Low Credit Limit Alert',
            f'Your credit limit is below 10%. Available: Rs.{remaining}',
            settings.EMAIL_HOST_USER,
            [user_email]
        )

@receiver(post_save, sender=Card)
def check_card_blocked(sender, instance, **kwargs):
    # 3. Card Blocked
    if instance.is_blocked:
        send_mail(
            'Card Blocked',
            f'Your card {instance.masked_number} has been blocked.',
            settings.EMAIL_HOST_USER,
            [instance.user.email]
        )