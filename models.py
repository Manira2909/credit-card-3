from django.db import models
from django.contrib.auth.models import User

# ============ RBAC ============
class Role(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Support', 'Support'),
        ('ReadOnly', 'Read-Only'),
    ]
    name = models.CharField(max_length=20, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_role')
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.role.name}"

# ============ CARD ============
class Card(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    card_holder = models.CharField(max_length=100)
    credit_limit = models.DecimalField(max_digits=10, decimal_places=2, default=50000)
    used_limit = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_blocked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def utilization(self):
        if self.credit_limit == 0:
            return 0
        return (float(self.used_limit) / float(self.credit_limit)) * 100

# ============ TRANSACTION + FRAUD ============
class Transaction(models.Model):
    FRAUD_STATUS = [
        ('SAFE', 'Safe'),
        ('FLAGGED', 'Flagged'),
        ('FRAUD', 'Fraud'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    card_last4 = models.CharField(max_length=4)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    merchant = models.CharField(max_length=100, default='Test Merchant')
    location = models.CharField(max_length=100, default='Chennai')
    device_id = models.CharField(max_length=100, default='device_1')
    category = models.CharField(max_length=50, default='Shopping')
    status = models.CharField(max_length=10, default='SUCCESS')
    fraud_status = models.CharField(max_length=10, choices=FRAUD_STATUS, default='SAFE')
    fraud_reason = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)

# ============ AUDIT LOG ============
class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('BLOCK', 'Card Block'),
        ('UNBLOCK', 'Card Unblock'),
        ('LIMIT_UPDATE', 'Limit Update'),
        ('FRAUD_FLAG', 'Fraud Flagged'),
    ]
    admin_user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, null=True)
    details = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(null=True)

    def __str__(self):
        return f"{self.admin_user} - {self.action} - {self.timestamp}"

# ============ SYSTEM HEALTH ============
class APILog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    endpoint = models.CharField(max_length=200)
    method = models.CharField(max_length=10)
    response_time_ms = models.FloatField()
    status_code = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)