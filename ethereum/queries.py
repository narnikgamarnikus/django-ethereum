from .models import Ethereum


def total_balance(user_id):
    eth = Ethereum.objects.filter(user__id=user_id)
    return sum([e.balance for e in eth])
