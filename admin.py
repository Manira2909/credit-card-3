from django.contrib import admin
from .models import Card, Transaction, Role, UserRole, AuditLog, APILog

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ['user', 'role']

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_number', 'credit_limit', 'used_limit', 'is_blocked', 'created_at']
    list_filter = ['is_blocked']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'card_last4', 'amount', 'merchant', 'fraud_status', 'date']
    list_filter = ['fraud_status', 'category']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['admin_user', 'action', 'details', 'timestamp']
    readonly_fields = ['timestamp']

@admin.register(APILog)
class APILogAdmin(admin.ModelAdmin):
    list_display = ['user', 'endpoint', 'method', 'response_time_ms', 'status_code', 'timestamp']
    readonly_fields = ['timestamp']