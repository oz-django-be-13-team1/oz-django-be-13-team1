
from django.db import models
from django.utils import timezone
from ..accounts.models import Accounts

class TransactionHistory(models.Model):

    # 계좌 정보
    account = models.ForeignKey(
        Accounts,
        on_delete=models.CASCADE,
        related_name='transaction_history',
        verbose_name = "계좌 정보"
    )

    # 거래 금액
    amount = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="거래 금액"
    )

    # 거래 후 잔액
    balance_after = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        verbose_name="거래 후 잔액"
    )

    # 계좌 인자 내역 (예: 오픈뱅킹 출금, ATM 입금, 나이키 결제 등)
    description = models.CharField(
        max_length=255,
        verbose_name="거래 내역 설명"
    )

    # 입출금 타입
    TRANSACTION_DIRECTION_CHOICES = [
        ("deposit", "입금"),
        ("withdrawal", "출금"),
    ]
    transaction_direction = models.CharField(
        max_length=20,
        choices=TRANSACTION_DIRECTION_CHOICES,
        verbose_name="입출금 타입"
    )

    # 거래 종류 (현금, 계좌이체, 자동이체, 카드결제 등)
    TRANSACTION_METHOD = [
        ("ATM", "ATM 거래"),
        ("TRANSFER", "계좌이체"),
        ("AUTOMATIC_TRANSFER", "자동이체"),
        ("CARD", "카드결제"),
        ("INTEREST", "이자"),
    ]

    # 거래 타입
    transaction_type = models.CharField(
        max_length=30,
        choices=TRANSACTION_METHOD,
        verbose_name="거래 타입"
    )

    # 거래 일시
    transaction_at = models.DateTimeField(
        default=timezone.now,
        verbose_name="거래 일시"
    )
    class Meta:
        db_table = 'transaction_history'
        verbose_name = "거래내역"
        verbose_name_plural = "거래내역 목록"
