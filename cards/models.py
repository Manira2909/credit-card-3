from django.db import models
from django.contrib.auth.models import User

class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16, unique=True)
    card_holder = models.CharField(max_length=100)
    expiry = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    used_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.card_holder} - {self.card_number[-4:]}"

    @property
    def available_limit(self):
        return self.credit_limit - self.used_limit

class Transaction(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant = models.CharField(max_length=100)
    description = models.CharField(max_length=200, default="Purchase")
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="Success")

    def __str__(self):
        return f"{self.merchant} - Rs.{self.amount}"