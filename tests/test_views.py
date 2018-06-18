from django.test import TestCase
from django.test import Client
from django.urls import reverse
from ethereum import models
from django.contrib.auth import get_user_model


class TestListView(TestCase):
    def setUp(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='user',
            password='password'
        )
        self.client = Client()
        self.eth = models.Ethereum.objects.create(user=user)

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/')
        self.assertRedirects(
            resp,
            '/accounts/login/?next=/',
            fetch_redirect_response=False
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='user', password='password')
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='user', password='password')
        resp = self.client.get(reverse('ethereum_list'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='user', password='password')
        resp = self.client.get(reverse('ethereum_list'))
        self.assertEqual(resp.status_code, 200)

        self.assertTemplateUsed(resp, 'ethereum/ethereum_list.html')

    def test_pagination(self):
        self.client.login(username='user', password='password')
        resp = self.client.get(reverse('ethereum_list'))
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)


class TestEthereumCreateView(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='user',
            password='password'
        )
        self.client = Client()

    def test_redirect_if_not_logged_in(self):
        resp = self.client.get('/create/')
        self.assertRedirects(
            resp,
            '/accounts/login/?next=/create/',
            fetch_redirect_response=False
        )

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='user', password='password')
        resp = self.client.get('/create/')
        self.assertTrue(
            models.Ethereum.objects.filter(user=self.user).exists()
        )
        self.assertEqual(resp.status_code, 302)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='user', password='password')
        resp = self.client.get(reverse('ethereum_create'))
        self.assertTrue(
            models.Ethereum.objects.filter(user=self.user).exists()
        )
        self.assertEqual(resp.status_code, 302)

    def test_view_uses_correct_template(self):
        self.client.login(username='user', password='password')
        resp = self.client.get(reverse('ethereum_create'))
        self.assertTrue(
            models.Ethereum.objects.filter(user=self.user).exists()
        )
        self.assertEqual(resp.status_code, 302)


class TestEthereumDetailView(TestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(
            username='user',
            password='password'
        )
        User.objects.create_user(
            username='user2',
            password='password'
        )
        self.client = Client()
        self.eth = models.Ethereum.objects.create(user=self.user)

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='user', password='password')
        resp = self.client.get('/1/')
        self.assertTrue(
            models.Ethereum.objects.filter(user=self.user).exists()
        )
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        self.client.login(username='user', password='password')
        resp = self.client.get(reverse('ethereum_detail', kwargs={'pk': 1}))
        self.assertTrue(
            models.Ethereum.objects.filter(user=self.user).exists()
        )
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='user', password='password')
        resp = self.client.get(reverse('ethereum_detail', kwargs={'pk': 1}))
        self.assertTrue(
            models.Ethereum.objects.filter(user=self.user).exists()
        )
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'ethereum/ethereum_detail.html')

    def test_context_data(self):
        self.client.login(username='user', password='password')
        resp = self.client.get(reverse('ethereum_detail', kwargs={'pk': 1}))
        self.assertTrue(
            'form' in resp.context
        )

    def test_permission_denies(self):

        self.client.login(username='user2', password='password')
        resp = self.client.get(reverse('ethereum_detail', kwargs={'pk': 1}))
        self.assertEqual(resp.status_code, 403)
        resp = self.client.post(
            reverse('ethereum_detail', kwargs={'pk': 1}),
            {
                'address': '0x16bDd33A3541cd1f42F54f6d37EDB769842f1502',
                'value': 0.0001,
                'gas': 1000
            }
        )
        self.assertEqual(resp.status_code, 403)

    def test_post(self):
        self.client.login(username='user', password='password')
        resp = self.client.post(
            reverse('ethereum_detail', kwargs={'pk': 1}),
            {
                'address': '0x16bDd33A3541cd1f42F54f6d37EDB769842f1502',
                'value': 0.0001,
                'gas': 1000
            }
        )
        resp = self.client.get(
            resp.url
        )
        messages = resp.context['messages']
        for message in messages:
            self.assertEqual(
                str(message),
                'Insufficient funds for gas * price + value'
            )
