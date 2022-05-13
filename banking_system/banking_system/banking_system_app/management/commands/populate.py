
from random import randint
import secrets
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from banking_system_app.models import Account, Ledger, AccountType, UserInformation
from banking_system_app.AccountRanks import AccountRanks
from django.utils import timezone
from django.conf import settings


class Command(BaseCommand):
    help = 'Populates the database with a central account and 2 users'

    def handle(self, **options):

        self.create_account_types()

        try:
            bank_user = User.objects.create_user('bank', email='', password=secrets.token_urlsafe(64))
            bank_user.is_active = False
            bank_user.save()
            rank = AccountType.objects.get(type=AccountRanks.BASIC)

            central_account_ipo = Account.objects.create(
                account_type=rank,
                user_id=bank_user,
                account_name="BANK IPO Account")

            central_account_ops = Account.objects.create(
                account_type=rank,
                user_id=bank_user,
                account_name="BANK OPS Account")
            central_account_ipo.save()
            central_account_ops.save()

            Ledger.transfer(
                10_000_000, central_account_ipo, "Initial amount", central_account_ops, "Initial amount", is_loan=True)

            self.create_users(2, central_account_ops)
            self.create_users(2, central_account_ops, is_staff=True)

        except CommandError as e:
            print(e)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Database'))

    def create_account_types(self):
        if not Account.objects.all():
            for type in AccountRanks:
                obj = AccountType.objects.create(type=type.value)
                obj.save()

    def create_users(self, num, ops_account, is_staff=False, account_rank: AccountRanks = AccountRanks.BASIC):
        for i in range(num):
            if not is_staff:
                username = f"Customer-{i}"
                email = f"customer{i}@test.com"
            else:
                username = f"Employe-{i}"
                email = f"employee{i}@test.com"

            user = User.objects.create(
                username=username,
                first_name=username,
                last_name=f"{username}ov",
                email=email, is_staff=is_staff)
            user.set_password('12345678')
            user.save()
            settings.TIME_ZONE
            date = timezone.datetime(2000, 5, 17)
            date = timezone.make_aware(date)

            user_info = UserInformation.objects.create(
                user_id=user.id,
                date_of_birth=date,
                cpr=f"{randint(0, 1_000_000_000)}",
                phone_number=f"{randint(0, 1_000_000_000)}")
            user_info.save()

            rank = AccountType.objects.get(type=account_rank.value)

            account = Account.objects.create(
                account_type=rank,
                user_id=user,
                account_name=username)
            account.save()

            Ledger.transfer(10_000, ops_account, "Initial ammount", account, "Initial ammount")
