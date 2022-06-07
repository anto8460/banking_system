from banking_system_app.models import AccountType, User, Account
from django.db.models import Q


def get_active_clients():
    return User.objects.filter(is_staff=False, is_active=True)


def get_unactive_clients():
    return User.objects.filter(is_staff=False, is_active=False)


def get_active_employees():
    return User.objects.filter(is_staff=True, is_active=True)


def get_unactive_employees():
    return User.objects.filter(Q(is_staff=True), Q(is_active=False), ~Q(username='bank'))


def get_account_types():
    return AccountType.objects.all()


def get_active_accounts():
    return Account.objects.filter(~Q(user_id=1), is_active=True)


def get_unactive_accounts():
    return Account.objects.filter(~Q(user_id=1), is_active=False)
