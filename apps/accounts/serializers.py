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
    # 테스트 코드를 위한 수정
    def create(self, validated_data):
        # 거래 생성 시 자동으로 잔액을 조정하는 로직
        account = validated_data["account"]
        amount = validated_data["amount"]
        t_type = validated_data["transaction_type"]

        # 입금: 계좌 잔액 증가
        if t_type == "deposit":
            account.balance += amount
            account.save()

        # 출금: 잔액 확인 후 차감
        elif t_type == "withdrawal":
            if account.balance < amount:
                raise serializers.ValidationError("잔액이 부족합니다.")
            account.balance -= amount
            account.save()

        # 거래 내역 생성
        transaction = Transaction.objects.create(**validated_data)
        return transaction