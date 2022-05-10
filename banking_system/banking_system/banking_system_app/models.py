
from decimal import Decimal
from django.contrib.auth.models import User
from django.db import models, transaction
from django.db.models.query import QuerySet
import uuid
from .errors import InsufficientFunds


class UID(models.Model):
    @classmethod
    @property
    def uid(cls):
        return cls.objects.create()

    def __str__(self):
        return f'{self.pk}'


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
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account_type = models.ForeignKey(AccountType, models.DO_NOTHING)
    user_id = models.ForeignKey(User, models.DO_NOTHING)
    account_number = models.CharField(unique=True, max_length=255)
    account_name = models.CharField(unique=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return f'Account - {self.account_number}'

    @property
    def movements(self) -> QuerySet:
        return Ledger.objects.filter(account=self)

    @property
    def balance(self) -> Decimal:
        return self.movements.aggregate(models.Sum('amount'))['amount__sum'] or Decimal(0)


class BankDetail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'bank_details'

    def __str__(self):
        return f'BankDetails - {self.id}'


class UserInformation(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    date_of_birth = models.DateTimeField()
    cpr = models.CharField(unique=True, max_length=10)
    phone_number = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'user_information'

    def __str__(self):
        return f'Information - {self.user.first_name} {self.user.last_name}: UserId {self.user}'


class Ledger(models.Model):
    account = models.ForeignKey(Account, on_delete=models.PROTECT)
    transaction = models.ForeignKey(UID, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    text = models.TextField()

    class Meta:
        db_table = 'ledger'

    @classmethod
    def transfer(cls, amount, debit_account, debit_text, credit_account, credit_text, is_loan=False) -> int:
        assert amount >= 0, 'Negative amount not allowed for transfer.'
        with transaction.atomic():
            if debit_account.balance >= amount or is_loan:
                uid = UID.uid
                cls(amount=-amount, transaction=uid, account=debit_account, text=debit_text).save()
                cls(amount=amount, transaction=uid, account=credit_account, text=credit_text).save()
            else:
                raise InsufficientFunds
        return uid

    def __str__(self):
        return f'{self.amount} :: {self.transaction} :: {self.created_at} :: {self.account} :: {self.text}'
