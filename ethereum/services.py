from django.conf import settings

from web3 import Web3, HTTPProvider

import requests


w3 = Web3(HTTPProvider('https://{}.infura.io/{}/'.format(
                       settings.NET,
                       settings.INFURA_API_KEY),
                       request_kwargs={'timeout': 60}))


def generate_new_address():
    address = w3.eth.account.create()
    return {
        'address': address.address,
        'private': address.privateKey.hex()
    }


def get_address_balance(address):
    assert type(address) is str, (
        'address must have a type str'
    )
    assert address[:2] == '0x', (
        'First two symbols of address must be 0x'
    )
    address = w3.toChecksumAddress(address)
    balance = w3.eth.getBalance(address)
    return w3.fromWei(balance, 'ether')


def get_transaction_list_from_address(address):
    assert type(address) is str, (
        'address must have a type str'
    )
    assert address[:2] == '0x', (
        'First two symbols of address must be 0x'
    )

    response = requests.get(
        'https://api{}.etherscan.io/api?module=account&action=txlist&address={}&startblock=0&endblock=latest&apikey={}'.format(
            '-rinkeby' if settings.NET == 'rinkeby' else '',
            address,
            settings.ETHERSCAN_API_KEY
        )
    )
    response_json = response.json()
    result = response_json['result']
    assert type(result) is list, (
        'List of result must be list'
    )
    return response_json['result']


def create_transaction(from_address, to_address, gas=90000,
                       gas_price='To-Be-Determined', value=0,
                       data=None, nonce=None):
    assert type(from_address) is str, (
        'from_address must have a type str'
    )
    assert from_address[:2] == '0x', (
        'First two symbols of from_address must be 0x'
    )
    assert type(to_address) is str, (
        'to_address must have a type str'
    )
    assert to_address[:2] == '0x', (
        'First two symbols of to_address must be 0x'
    )
    from_address = w3.toChecksumAddress(from_address)
    to_address = w3.toChecksumAddress(to_address)

    if not nonce:
        nonce = w3.eth.getTransactionCount(from_address)

    transaction = {
        'nonce': nonce,
        'gasPrice': w3.eth.gasPrice,
        'gas': gas,
        'to': to_address,
        'value': w3.toWei(value, 'ether'),
        'data': data if data else b'',
    }
    return transaction


def sign_transaction(transaction, private_key):
    signed_transaction = w3.eth.account.signTransaction(
        transaction, private_key
    )
    return signed_transaction


def send_transaction(signed_transaction):
    tx_hash = w3.eth.sendRawTransaction(signed_transaction.rawTransaction)
    return tx_hash.hex()


def get_ethereum_coinmarketcap_price():
    response = requests.get('https://api.coinmarketcap.com/v2/ticker/')
    response_json = response.json()
    for item in response_json['data']:
        if response_json['data'][item]['name'] == 'Ethereum':
            return response_json['data'][item]['quotes']['USD']['price']
