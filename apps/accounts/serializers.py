from rest_framework import serializers
from .models import Accounts

class AccountsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accounts
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

        # 잔액, 계좌번호 등 핵심 정보는 생성 후 수정 불가능
        read_only_fields = [
            "account_id",
            "user",
            "account_number",
            "bank_code",
            "account_type",
            "balance",  # 잔액은 거래를 통해서만 변경
            "created_at",
            "updated_at"
        ]
