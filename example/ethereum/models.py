# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.urls import reverse

from .services import (generate_new_address, get_address_balance,
                       get_transaction_list_from_address,
                       create_transaction, sign_transaction,
                       send_transaction, get_ethereum_coinmarketcap_price)


class Ethereum(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    address = models.CharField(max_length=42)
    private = models.CharField(max_length=66)

    def save(self, *args, **kwargs):
        if not self.pk:
            new_address = generate_new_address()
            self.address = new_address['address']
            self.private = new_address['private']
        return super(Ethereum, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('ethereum_detail', kwargs={'pk': self.pk})

    @property
    def balance(self):
        return get_address_balance(self.address)

    @property
    def transactions(self):
        return get_transaction_list_from_address(self.address)

    def spend(self, to_address, gas=90000, gas_price='To-Be-Determined', value=0,
              data=None, nonce=None):
        transaction = create_transaction(from_address=self.address,
                                         to_address=to_address,
                                         gas=90000,
                                         gas_price='To-Be-Determined',
                                         value=0, data=None, nonce=None)
        signed_transaction = sign_transaction(transaction, self.private)
        tx_hash = send_transaction(signed_transaction)
        return tx_hash

    @property
    def price(self):
        return get_ethereum_coinmarketcap_price()
