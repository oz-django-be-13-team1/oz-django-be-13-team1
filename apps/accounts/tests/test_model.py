from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from decimal import Decimal

from apps.accounts.models import Account
from apps.accounts.constants import BANK_CODES, ACCOUNT_TYPE

User = get_user_model()

BANK_VALID_CODE = BANK_CODES[0][0]
ACCOUNT_VALID_TYPE = ACCOUNT_TYPE[0][0]

class AccountsModelTests(TestCase):
    """Accounts 모델의 기본 제약 조건 및 유효성 검증"""

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(email='acc_test@user.com', password='password123')

    def make_account(self, **overrides):
        """기본값 + 오버라이드 값으로 계좌 생성 헬퍼"""
        data = {
            'user': self.user,
            'account_number': '1104567890',
            'bank_code': BANK_VALID_CODE,
            'account_type': ACCOUNT_VALID_TYPE,
            'balance': Decimal('0.00'),
        }
        data.update(overrides)
        return Account(**data)

    def test_account_number_unique(self):
        """계좌번호는 중복 생성 불가"""
        self.make_account(account_number='1234').save()
        with self.assertRaises(IntegrityError):
            self.make_account(account_number='1234').save()

    def test_default_balance_zero(self):
        """기본 잔액은 0원이어야만 한다"""
        account = self.make_account(account_number='5678')
        account.save()
        self.assertEqual(account.balance, Decimal('0.00'))

    def test_invalid_account_number_raises_error(self):
        """계좌번호에 숫자가 아닌 값이 들어가면 ValidationError 발생"""
        account = self.make_account(account_number='abcde')
        with self.assertRaises(ValidationError):
            account.full_clean()

    def test_negative_balance_not_allowed(self):
        """음수 잔액은 허용하면 안돼"""
        account = self.make_account(balance=Decimal('-100.00'))
        with self.assertRaises(ValidationError):
            account.full_clean()

    def test_invalid_bank_code_choice(self):
        """bank_code에 정의되지 않은 값은 ValidationError 발생"""
        account = self.make_account(bank_code='999')
        with self.assertRaises(ValidationError):
            account.full_clean()

    def test_invalid_account_type_choice(self):
        """account_type에 정의되지 않은 값은 ValidationError 발생"""
        account = self.make_account(account_type='INVALID')
        with self.assertRaises(ValidationError):
            account.full_clean()
