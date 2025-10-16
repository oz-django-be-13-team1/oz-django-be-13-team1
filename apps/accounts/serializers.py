from rest_framework import serializers
from .models import Account, Transaction

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = [
            "account_id",
            "user",
            "account_number",
            "bank_code",
            "account_type",
            "balance",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "account_id",
            "account_number",
            "bank_code",
            "account_type",
            "balance",  # 잔액은 거래를 통해서만 변경
            "created_at",
            "updated_at",
        ]

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction  # Transaction 모델로 수정
        fields = [
            "id",
            "account",
            "user",
            "transaction_type",
            "amount",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "user",
            "created_at",
        ]
