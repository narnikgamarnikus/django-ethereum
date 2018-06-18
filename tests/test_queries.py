from django.test import TestCase
from django.contrib.auth import get_user_model

from ethereum.queries import total_balance
from ethereum.models import Ethereum


class TestTotalBalance(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='username', password='password')

    def test_with_eth(self):
        self.eth = Ethereum.objects.create(user=self.user)
        balance = total_balance(self.user.id)
        self.assertEqual(balance, 0)

    def test_without_eth(self):
        balance = total_balance(self.user.id)
        self.assertEqual(balance, 0)
