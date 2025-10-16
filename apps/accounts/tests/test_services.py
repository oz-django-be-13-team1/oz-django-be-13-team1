from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.accounts.models import Account, Transaction  # TransactionHistory로 변경 권장

User = get_user_model()


class TransactionAPITests(TestCase):
    """
    TransactionViewSet의 입금/출금/잔액 부족/원자성 로직을
    실제 API 호출 방식으로 검증
    """

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(email='api@test.com', password='password')
        self.account = Account.objects.create(
            user=self.user,
            account_number="1234567890",
            bank_code="004",
            account_type="CHECKING",
            balance=Decimal("1000.00")
        )
        self.deposit_amount = Decimal("500.00")
        self.withdrawal_amount = Decimal("200.00")
        # 인증
        self.client.force_authenticate(user=self.user)

    # ------------------------- Helper -------------------------
    def post_transaction(self, amount, transaction_type):
        """TransactionViewSet에 거래 요청 보내기"""

        url = reverse("accounts:transactions-list")

        return self.client.post(
            url,
            {
                "account": self.account.account_id,
                "amount": amount,
                "transaction_type": transaction_type,
                "user": self.user.pk
            },
            format="json"
        )

    # ------------------------- 입금 테스트 -------------------------
    def test_deposit_updates_balance_and_creates_transaction(self):
        response = self.post_transaction(self.deposit_amount, "deposit")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1500.00"))

        transaction = Transaction.objects.get(account=self.account)
        self.assertEqual(transaction.amount, self.deposit_amount)
        self.assertEqual(transaction.transaction_type, "deposit")

    # ------------------------- 출금 테스트 -------------------------
    def test_withdrawal_updates_balance_and_creates_transaction(self):
        response = self.post_transaction(self.withdrawal_amount, "withdrawal")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("800.00"))

        transaction = Transaction.objects.get(account=self.account)
        self.assertEqual(transaction.amount, self.withdrawal_amount)
        self.assertEqual(transaction.transaction_type, "withdrawal")

    # ------------------------- 잔액 부족 테스트 -------------------------
    def test_withdrawal_fail_on_insufficient_balance(self):
        response = self.post_transaction(Decimal("1500.00"), "withdrawal")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1000.00"))
        self.assertEqual(Transaction.objects.count(), 0)

    # ------------------------- 원자성 테스트 -------------------------
    # GPT는 신이야

    @patch("apps.accounts.serializers.TransactionSerializer.save")
    def test_atomic_failure_rolls_back(self, mock_save):
        # serializer.save() 호출 시 강제로 예외 발생
        mock_save.side_effect = Exception("강제 오류 발생")

        # Exception 발생을 assertRaises로 잡음
        with self.assertRaises(Exception):
            self.post_transaction(self.deposit_amount, "deposit")

        # DB 롤백 확인: 계좌 잔액은 변경되지 않아야 함
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1000.00"))

        # DB 롤백 확인: 트랜잭션도 생성되지 않아야 함
        self.assertEqual(Transaction.objects.count(), 0)
