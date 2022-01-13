from django.contrib.auth.models import User
from django.db.utils import IntegrityError
from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .models import Account
from .views import AccountBalanceView, DepositView, WithdrawalView

# Create your tests here.


class AccountModelTestCase(TestCase):
    def setUp(self):
        """Set up data for testing"""
        user = User.objects.create(username="test")
        Account.objects.create(user=user)

    def test_creates_with_default_values(self):
        """Asserts create an account with default values"""
        account = Account.objects.get(pk=1)
        self.assertEqual(account.is_active, True)
        self.assertEqual(account.balance, 0.0)

    def test_asserts_user_is_required(self):
        """Asserts an associated user is required"""
        with self.assertRaises(IntegrityError):
            Account.objects.create()


class ApiTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        user = User.objects.create(username="test")
        Account.objects.create(user=user)
        user = User.objects.create(username="test2")
        Account.objects.create(balance=100.0, user=user)

    def test_balance_no_auth(self):
        """Asserts non authenticated users cannot check their balance"""
        request = self.factory.get("/api/v1/balance/")
        response = AccountBalanceView.as_view()(request)
        self.assertEqual(response.status_code, 401)

    def test_balance_with_auth(self):
        """Assets authenticated users can check their balance"""
        for pk, balance in [(1, 0.00), (2, 100.00)]:
            request = self.factory.get("/api/v1/balance/")
            user = User.objects.get(pk=pk)
            force_authenticate(request, user=user)
            response = AccountBalanceView.as_view()(request)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(float(response.data.get("balance")), balance)

    def test_deposit_unknown_account(self):
        """Asserts error response when make a deposit to an unknown account"""
        request = self.factory.put("/api/v1/deposit/", {"amount": 50.0})
        response = DepositView.as_view()(request, username="inexistent")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data.get("message"), "account not found")

    def test_deposit_existent_account(self):
        """Asserts make a deposit to an account"""
        request = self.factory.put("/api/v1/deposit/", {"amount": 50.0})
        response = DepositView.as_view()(request, username="test")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("message"), "deposit made")
        self.assertEqual(response.data.get("new_balance"), 50.0)

    def test_deposit_sum(self):
        """Asserts sums two consecutives deposits"""
        for amount, new_balance in [(15.0, 15.0), (35.0, 50.0)]:
            request = self.factory.put("/api/v1/deposit/", {"amount": amount})
            response = DepositView.as_view()(request, username="test")
            self.assertEqual(response.status_code, 201)
            self.assertEqual(response.data.get("message"), "deposit made")
            self.assertEqual(response.data.get("new_balance"), new_balance)

    # def test_deposit_max(self):

    def test_withdrawal_no_auth(self):
        """Asserts non authenticated users cannot withdraw money"""
        request = self.factory.get("/api/v1/withdrawal/")
        response = AccountBalanceView.as_view()(request, pk=1)
        self.assertEqual(response.status_code, 401)

    def test_withdrawal_with_auth(self):
        """Asserts authenticated users can withdraw money"""
        request = self.factory.put("/api/v1/withdrawal/", {"amount": 90.0})
        user = User.objects.get(pk=2)
        force_authenticate(request, user=user)
        response = WithdrawalView.as_view()(request)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data.get("message"), "withdrawal made")
        self.assertEqual(response.data.get("balance"), 10.0)
