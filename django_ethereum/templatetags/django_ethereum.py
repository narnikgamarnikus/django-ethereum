from django import template
from ..queries import total_balance
from ..services import get_ethereum_coinmarketcap_price

register = template.Library()


@register.simple_tag(takes_context=True)
def request_user_total_balance(context):
    request = context.get('request', None)
    if request:
        request_user = hasattr(request, 'user')
        if request_user:
            user = request.user
            if user.is_authenticated:
                balance = total_balance(user.id)
                return balance


@register.simple_tag(takes_context=True)
def request_user_total_balance_usd(context):
    request = context.get('request', None)
    if request:
        request_user = hasattr(request, 'user')
        if request_user:
            user = request.user
            if user.is_authenticated:
                balance = total_balance(user.id)
                return balance * get_ethereum_coinmarketcap_price()
