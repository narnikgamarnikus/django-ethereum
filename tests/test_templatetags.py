from django.test import TestCase
from django.test import RequestFactory
from django.template import Context, Template
from django.contrib.auth import get_user_model

from ethereum import models
from ethereum.templatetags import ethereum


class TestRequestUserTotalBalance(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='user',
            password='password'
        )
        self.eth = models.Ethereum.objects.create(user=self.user)

    def test_with_request_user(self):
        request_factory = RequestFactory()
        request = request_factory.get('/')
        request.user = self.user

        out = Template(
            "{% load ethereum %}"
            "{% request_user_total_balance %}"
        ).render(Context({
            'request': request,
            })
        )

        self.assertEqual(
            out,
            '0'
        )

    def test_without_request_user(self):
        request_factory = RequestFactory()
        request = request_factory.get('/')

        out = Template(
            "{% load ethereum %}"
            "{% request_user_total_balance %}"
        ).render(Context({
            'request': request,
            })
        )

        self.assertEqual(
            out,
            'None'
        )


class TestRequestUserTotalBalanceUsd(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='user',
            password='password'
        )
        self.eth = models.Ethereum.objects.create(user=self.user)

    def test_with_request_user(self):
        request_factory = RequestFactory()
        request = request_factory.get('/')
        request.user = self.user

        out = Template(
            "{% load ethereum %}"
            "{% request_user_total_balance_usd %}"
        ).render(Context({
            'request': request,
            })
        )

        self.assertEqual(
            out,
            '0.0'
        )

    def test_without_request_user(self):
        request_factory = RequestFactory()
        request = request_factory.get('/')

        out = Template(
            "{% load ethereum %}"
            "{% request_user_total_balance_usd %}"
        ).render(Context({
            'request': request,
            })
        )

        self.assertEqual(
            out,
            'None'
        )
