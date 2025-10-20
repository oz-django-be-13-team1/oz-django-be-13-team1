from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator
from django.conf import settings

import uuid

from .constants import BANK_CODES, ACCOUNT_TYPE

User = get_user_model()


class Account(models.Model):

    account_id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
        verbose_name="계좌 ID"
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name="소유자"
    )

    account_number = models.CharField(
        max_length=20,
        unique=True,
        validators=[RegexValidator(regex=r'^\d+$', message='계좌번호는 숫자만 입력 가능합니다.')],
        verbose_name="계좌번호"
    )

    bank_code = models.CharField(
        max_length=3,
        choices=BANK_CODES,
        verbose_name="은행 코드"
    )

    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE,
        verbose_name="계좌 유형"
    )

    balance = models.DecimalField(
        max_digits=18,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(0)],
        verbose_name="잔액"
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="생성일시"
    )

    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="수정일시"
    )

    class Meta:
        db_table = 'accounts'
        verbose_name = '계좌'
        verbose_name_plural = '계좌'

    def __str__(self):
        return f"{self.user} - {self.account_number}"

class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10)  # 예: deposit, withdraw
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.amount} - {self.transaction_type}"
