
import django_rq
import uuid
import requests
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.query import QuerySet
from django.utils import timezone
from .errors import InsufficientFunds, UnAuthorized
from .AccountRanks import AccountRanks
from banking_system_app.Utils.generators import generate_account_number, generate_routing_number
from rest_framework.authtoken.models import Token


class UID(models.Model):

    @classmethod
    @property
    def uid(cls):
        return cls.objects.create()

    def __str__(self):
        return f'{self.pk}'


class KnownBank(models.Model):
    routing_number = models.CharField(primary_key=True, max_length=3, editable=False, default=generate_routing_number)
    user = models.ForeignKey(User, models.DO_NOTHING)
    address = models.CharField(max_length=15)
    port = models.CharField(max_length=4)
    name = models.CharField(max_length=255)
    is_local = models.BooleanField(default=False)

    def __str__(self):
        return f'KnownBank - {self.address}:{self.port} - {self.name}'

    class Meta:
        db_table = 'known_banks'


class AccountType(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    type = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'AccountType - {self.type}'

    class Meta:
        db_table = 'account_types'


class Account(models.Model):
    id = models.CharField(max_length=9, primary_key=True, editable=False, default=generate_account_number)
    account_type = models.ForeignKey(AccountType, models.DO_NOTHING)
    user_id = models.ForeignKey(User, models.DO_NOTHING)
    routing_number = models.ForeignKey(KnownBank, models.DO_NOTHING)
    account_name = models.CharField(unique=False, max_length=255)
    is_active = models.BooleanField(unique=False)
    use_mfa = models.BooleanField(unique=False, default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return f'Account - {self.routing_number.routing_number}:{self.id} -{self.account_name}'

    @property
    def account_number(self):
        return f'{self.routing_number.routing_number} - {self.id}'

    @property
    def movements(self) -> QuerySet:
        return Ledger.objects.filter(account=self)

    @property
    def balance(self) -> Decimal:
        return self.movements.aggregate(models.Sum('amount'))['amount__sum'] or Decimal(0)

    def make_loan(self, amount):

        if self.account_type.type == AccountRanks.BASIC.value:
            raise UnAuthorized("Credit account can't loan from the bank")

        debit_account = Account(
            account_type=AccountType.objects.get(type=AccountRanks.LOAN.value),
            user_id=self.user_id,
            account_name='Loan',
            is_active=True,
            created_at=timezone.now())

        debit_account.save()

        Ledger.transfer(amount, debit_account, 'loan', self, 'loan', is_loan=True)


class UserInformation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    date_of_birth = models.DateTimeField()
    cpr = models.CharField(unique=True, max_length=10)
    phone_number = models.CharField(unique=True, max_length=255)
    is_active = models.BooleanField(default=True)
    use_mfa = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_information'

    def __str__(self):
        return f'Information - {self.user.first_name} {self.user.last_name}: UserId {self.user}'


class TransferRequests(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    from_account = models.ForeignKey(Account, related_name='from_account', on_delete=models.CASCADE)
    to_account = models.ForeignKey(Account, related_name='to_account', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    text = models.TextField()
    is_new = models.BooleanField(default=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        db_table = 'transfer_requests'

    def __str__(self):
        return f'Transfer request from account: {self.from_account} to account: {self.to_account}'

class Ledger(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    transaction = models.ForeignKey(UID, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    text = models.TextField()

    class Meta:
        db_table = 'ledger'

    @classmethod
    def intra_transfer(cls, amount, debit_account, debit_text, credit_account, credit_text, is_loan=False) -> int:
        assert amount >= 0, 'Negative amount not allowed for transfer.'
        with transaction.atomic():
            if debit_account.balance >= amount or is_loan:
                uid = UID.uid
                cls(amount=-amount, transaction=uid, account=debit_account, text=debit_text).save()
                cls(amount=amount, transaction=uid, account=credit_account, text=credit_text).save()
            else:
                raise InsufficientFunds
        return uid

    @classmethod
    def inter_transfer(
          cls,
          amount: float,
          sender: Account,
          sender_text: str,
          reciever: str,
          known_bank: KnownBank) -> bool:
        
        ip = known_bank.address
        port = known_bank.port

        token = Token.objects.get(user_id=known_bank.user)

        headers = {
            'Authorization': f'Token {token.key}'
        }

        has_address = requests.get(f'http://{ip}:{port}/api/v1/account/{reciever}', headers=headers)

        if has_address.status_code == 200:
            transaction_text = f"Transaction from: {sender.account_number}\n" + sender_text

            body = {
                'amount': amount,
                'account_id': reciever,
                'text': transaction_text
            }

            response = requests.post(f'http://{ip}:{port}/api/v1/inter-transaction', data=body, headers=headers)

            if response.status_code == 200:
                transaction_text = f"Transaction to: {known_bank.routing_number} - {reciever}\n" + sender_text
                uid = UID.uid
                cls(amount=-float(amount), transaction=uid, account=sender, text=transaction_text).save()

                return True

        return False

    def __str__(self):
        return f'{self.amount} :: {self.transaction} :: {self.created_at} :: {self.account} :: {self.text}'
