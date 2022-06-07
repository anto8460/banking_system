import string
from random import choices
# from banking_system_app.models import Account, KnownBank


# Account number will be 9 digits
def generate_account_number():
    account_number = ''.join(choices(string.ascii_uppercase + string.digits, k=9))
    return account_number


# routing number will be 3 digits
def generate_routing_number():
    route_number = ''.join(choices(string.ascii_uppercase + string.digits, k=3))
    return route_number
