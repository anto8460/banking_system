# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.contrib.auth.models import User
import uuid


class AccountType(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    type = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
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
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return f'Account - {self.account_number}'

    def get_balance(self):
        transactions = AccountsTransaction.objects.filter(account=self.id)
        balance = 0
        for transaction in transactions:
            balance += Transaction.objects.get(id=transaction.transaction.id).amount
        return balance


class AccountsTransaction(models.Model):
    account = models.OneToOneField(Account, models.DO_NOTHING, primary_key=True, default=uuid.uuid4)
    transaction = models.ForeignKey('Transaction', models.DO_NOTHING)

    class Meta:
        db_table = 'accounts_transactions'
        unique_together = (('account', 'transaction'),)


class BankDetail(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    created_at = models.DateTimeField()
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
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'user_information'

    def __str__(self):
        return f'Information - {self.user.first_name} {self.user.last_name}: UserId {self.user}'


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    customer = models.ForeignKey(User, models.DO_NOTHING)
    amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'loans'

    def __str__(self):
        return f'Loan - {self.customer} - {self.amount}'


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    amount = models.FloatField()
    text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'transactions'
