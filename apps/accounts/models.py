from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator, MinValueValidator
import uuid

# choices는 constants.py로 분리
from .constants import BANK_CODES, ACCOUNT_TYPE

User = get_user_model()


class Accounts(models.Model):
    """
    계좌 정보를 저장하는 모델
    - User와 1:N 관계
    - TransactionHistory와 1:N 관계 예정 (외래키 대상)
    """
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
