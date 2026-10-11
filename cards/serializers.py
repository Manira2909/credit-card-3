from rest_framework import serializers
from.models import CreditCard, Transaction

class CreditCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CreditCard
        fields = ['id', 'holder_name', 'last4', 'expiry_month', 'expiry_year', 'is_active']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'