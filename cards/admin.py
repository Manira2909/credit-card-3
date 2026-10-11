from django.contrib import admin
from .models import Card, Transaction

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'card_holder', 'get_masked_number', 'credit_limit', 'used_limit', 'is_blocked', 'created_at')
    list_filter = ('is_blocked', 'created_at')
    search_fields = ('card_number', 'card_holder', 'user__username')

    def get_masked_number(self, obj):
        return f"**** **** **** {obj.card_number[-4:]}"
    get_masked_number.short_description = 'Card Number'

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'merchant', 'amount', 'date', 'status')
    list_filter = ('status', 'date')