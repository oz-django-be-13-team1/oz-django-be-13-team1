from decimal import Decimal
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from apps.accounts.models import Account, Transaction

User = get_user_model()

class AccountTransactionAPITests(TestCase):
    """
    AccountViewSet / TransactionViewSet 테스트
    - 계좌 조회, 삭제
    - 거래 생성(입금/출금)
    - 거래 조회
    """

    def setUp(self):
        """
        테스트 준비 단계
        - 테스트용 사용자 2명 생성
        - 테스트용 계좌 2개 생성(다른 사용자)
        - APIClient로 인증 설정
        """
        self.client = APIClient()
        self.user = User.objects.create_user(email="testuser@example.com", password="password")
        self.other_user = User.objects.create_user(email="otheruser@example.com", password="password")

        # 테스트용 계좌 생성
        self.account = Account.objects.create(
            user=self.user, # 내 계좌
            account_number="1234567890",
            bank_code="004",
            account_type="CHECKING",
            balance=Decimal("1000.00")
        )
        self.other_account = Account.objects.create(
            user=self.other_user, # 다른 사람 계좌
            account_number="0987654321",
            bank_code="004",
            account_type="CHECKING",
            balance=Decimal("500.00")
        )

        # 테스트 클라이언트에 로그인된 사용자 설정
        self.client.force_authenticate(user=self.user)

    # -------------------- 반복적으로 쓰이는 동작들 -----------------------
    # GPT 최고
    def post_transaction(self, account_id, amount, transaction_type):
        """
        거래를 post 요청으로 생성하는 함수
        - account_id: 거래할 계좌
        - amount: 금액
        - transaction_type: 'deposit' 또는 'withdrawal'
        """
        url = reverse("accounts:transactions-list")
        return self.client.post(
            url,
            {
                "account": account_id,
                "amount": str(amount),
                "transaction_type": transaction_type
            },
            format="json"
        )

    # ------------------------- 계좌 테스트 -------------------------
    def test_account_list(self):
        """GET /accounts/ : 본인 계좌만 조회 가능한지 테스트"""
        url = reverse("accounts:accounts-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # 본인 계좌만 조회
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["account_number"], self.account.account_number)

    def test_account_retrieve(self):
        """GET /accounts/{account_id}/ : 특정 계좌 상세 조회 테스트"""
        url = reverse("accounts:accounts-detail", args=[self.account.account_id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["account_number"], self.account.account_number)

    def test_account_destroy_with_zero_balance(self):
        """DELETE /accounts/{account_id}/ : 계좌 잔액이 0일 때 삭제 가능"""
        self.account.balance = Decimal("0.00")
        self.account.save()
        url = reverse("accounts:accounts-detail", args=[self.account.account_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # DB에서 계좌 삭제되었는지 확인
        self.assertFalse(Account.objects.filter(account_id=self.account.account_id).exists())

    def test_account_destroy_with_nonzero_balance(self):
        """DELETE /accounts/{account_id}/ : 잔액 남아있는 계좌는 삭제 불가 """
        url = reverse("accounts:accounts-detail", args=[self.account.account_id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # 계좌는 여전히 DB에 존재해야 함
        self.assertTrue(Account.objects.filter(account_id=self.account.account_id).exists())

    # ------------------------- 거래 테스트 -------------------------
    def test_deposit_transaction(self):
        """거래 생성 테스트(입금): 입금 후 계좌 잔액 증가, transaction 객체 생성 확인"""
        response = self.post_transaction(self.account.account_id, Decimal("500.00"), "deposit")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1500.00"))
        transaction = Transaction.objects.get(account=self.account)
        self.assertEqual(transaction.amount, Decimal("500.00"))
        self.assertEqual(transaction.transaction_type, "deposit")

    def test_withdrawal_transaction(self):
        """거래 생성 테스트 (출금): 출금 후 계좌 잔액 감소, transaction 객체 생성 확인"""
        response = self.post_transaction(self.account.account_id, Decimal("200.00"), "withdrawal")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("800.00"))
        transaction = Transaction.objects.get(account=self.account)
        self.assertEqual(transaction.amount, Decimal("200.00"))
        self.assertEqual(transaction.transaction_type, "withdrawal")

    def test_withdrawal_insufficient_balance(self):
        """출금 테스트 (잔액 부족): 잔액 보다 많은 금액 출금 시 에러 발생, 계좌 잔액과 transaction 객체 변화 X"""
        response = self.post_transaction(self.account.account_id, Decimal("1500.00"), "withdrawal")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.account.refresh_from_db()
        self.assertEqual(self.account.balance, Decimal("1000.00"))
        self.assertEqual(Transaction.objects.count(), 0)

    def test_transaction_list_only_user_account(self):
        # 다른 사용자의 거래 생성
        Transaction.objects.create(
            account=self.other_account,
            user=self.other_user,
            transaction_type="deposit",
            amount=Decimal("100.00")
        )
        # 본인 계좌 거래 생성
        Transaction.objects.create(
            account=self.account,
            user=self.user,
            transaction_type="deposit",
            amount=Decimal("200.00")
        )
        url = reverse("accounts:transactions-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["amount"], "200.00")
