# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
import uuid
from django.db import models
from django.contrib.auth.models import User


class AccountType(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    type = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f'AccountType - {self.type}'

    class Meta:
        db_table = 'account_types'


class Account(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    account_type = models.ForeignKey(AccountType, models.DO_NOTHING)
    customer = models.ForeignKey('Customer', models.DO_NOTHING)
    account_number = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'accounts'

    def __str__(self):
        return f'Account - {self.account_number}'


class AccountsTransaction(models.Model):
    account = models.OneToOneField(Account, models.DO_NOTHING, primary_key=True)
    transaction = models.ForeignKey('Transaction', models.DO_NOTHING)

    class Meta:
        db_table = 'accounts_transactions'
        unique_together = (('account', 'transaction'),)


class BankDetail(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    account = models.ForeignKey(Account, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'bank_details'

    def __str__(self):
        return f'BankDetails - {self.id}'


class Customer(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    cpr = models.CharField(unique=True, max_length=10)
    age = models.IntegerField()
    phone_number = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'customers'

    def __str__(self):
        return f'Customer - {self.first_name} {self.last_name}: UserId {self.user}'


class Employee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    cpr = models.CharField(unique=True, max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f'Employee - {self.first_name} {self.last_name}: UserId {self.user.username}'


class Loan(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    customer = models.ForeignKey(Customer, models.DO_NOTHING)
    amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        db_table = 'loans'

    def __str__(self):
        return f'Loan - {self.customer} - {self.amount}'


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(), editable=False)
    amount = models.FloatField()
    text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        db_table = 'transactions'
