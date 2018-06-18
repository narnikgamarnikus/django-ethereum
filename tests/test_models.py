#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_django-ethereum
------------

Tests for `django-ethereum` models module.
"""

from django.test import TestCase

from ethereum import models
from django.contrib.auth import get_user_model


class TestEthereum(TestCase):

    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='user',
            password='password'
        )
        self.eth = models.Ethereum.objects.create(user=user)

    def test_address_and_private_is_exists(self):
        self.assertTrue(
            self.eth.address.startswith('0x')
        )
        self.assertEqual(
            len(self.eth.address),
            42
        )

        self.assertTrue(
            self.eth.private.startswith('0x')
        )
        self.assertEqual(
            len(self.eth.private),
            66
        )

    def test_balance_property(self):
        self.assertEqual(
            self.eth.balance,
            0
        )

    def test_balance_transactions(self):
        self.assertEqual(
            self.eth.transactions,
            []
        )

    def test_price(self):
        self.assertTrue(self.eth.price > 0)

    def tearDown(self):
        pass
