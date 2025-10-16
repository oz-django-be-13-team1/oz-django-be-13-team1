from rest_framework import serializers
from .models import TransactionHistory

class TransactionHistorySerializer(serializers.ModelSerializer):
    account_number = serializers.CharField(source='account.account_number', read_only=True)

    class Meta:
        model = TransactionHistory
        fields = [
            "id",
            "account_number",
            "transaction_direction",
            "transaction_type",
            "amount",
            "balance_after",
            "description",
            "transaction_at"
        ]
        read_only_fields = [
            "id",
            "transaction_at",
            "balance_after",
        ]
