from django.test import TestCase
from ethereum import forms


class TestEthereumPayForm(TestCase):

    def setUp(self):
        pass

    def test_with_valid_data(self):
        data = {
            'address': '0x16bDd33A3541cd1f42F54f6d37EDB769842f1502',
            'value': 0.0001,
            'gas': 1000
        }
        form = forms.EthereumPayForm(data=data)
        self.assertTrue(form.is_valid())

    def test_with_invalid_address(self):
        data = {
            'address': 'FAKE_ADDRESS',
            'value': 0.0001,
            'gas': 1000
        }
        form = forms.EthereumPayForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['address'].__repr__()[2:-2],
            'First two symbols of address must be 0x.'
        )

    def test_with_invalid_value(self):
        data = {
            'address': '0x16bDd33A3541cd1f42F54f6d37EDB769842f1502',
            'value': 'FAKE_VALUE',
            'gas': 1000
        }
        form = forms.EthereumPayForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['value'].__repr__()[2:-2],
            'Enter a number.'
        )

    def test_with_invalid_gas(self):
        data = {
            'address': '0x16bDd33A3541cd1f42F54f6d37EDB769842f1502',
            'value': 1000,
            'gas': 0.1
        }
        form = forms.EthereumPayForm(data=data)
        self.assertFalse(form.is_valid())
        self.assertEqual(
            form.errors['gas'].__repr__()[2:-2],
            'Enter a whole number.'
        )
