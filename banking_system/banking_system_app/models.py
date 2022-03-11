# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AccountTypes(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    type = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'account_types'


class Accounts(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    account_type = models.ForeignKey(AccountTypes, models.DO_NOTHING)
    customer = models.ForeignKey('Customers', models.DO_NOTHING)
    account_number = models.CharField(unique=True, max_length=255)
    balance = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'accounts'


class AccountsTransactions(models.Model):
    account = models.OneToOneField(Accounts, models.DO_NOTHING, primary_key=True)
    transaction = models.ForeignKey('Transactions', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'accounts_transactions'
        unique_together = (('account', 'transaction'),)


class BankDetails(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    account = models.ForeignKey(Accounts, models.DO_NOTHING)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bank_details'


class Customers(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user = models.OneToOneField('Users', models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    cpr = models.CharField(unique=True, max_length=8)
    age = models.IntegerField()
    phone_number = models.CharField(unique=True, max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customers'


class Employees(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    user = models.ForeignKey('Users', models.DO_NOTHING)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(unique=True, max_length=255)
    cpr = models.CharField(unique=True, max_length=8)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'employees'


class Loans(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    customer = models.ForeignKey(Customers, models.DO_NOTHING)
    amount = models.FloatField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'loans'


class Transactions(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    amount = models.FloatField()
    text = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'transactions'


class Users(models.Model):
    id = models.CharField(primary_key=True, max_length=36)
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'users'
