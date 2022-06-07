
from random import randint
import secrets
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from banking_system_app.models import Account, Ledger, AccountType, UserInformation, KnownBank
from rest_framework.authtoken.models import Token
from banking_system_app.AccountRanks import AccountRanks
from django.utils import timezone
from django.conf import settings


class Command(BaseCommand):
    help = 'Populates the database with a central account and 2 users'

    def handle(self, **options):

        self.create_account_types()

        try:
            super_user = User.objects.create_superuser('admin', 'admin@gmail.com', 'admin')
            super_user.save()

            bank_user = User.objects.create_user('bank', email='', password=secrets.token_urlsafe(64))
            bank_user.save()
            rank = AccountType.objects.get(type=AccountRanks.BASIC)

            foreign_bank_user = User.objects.create_user('bank2', email='', password=secrets.token_urlsafe(64))
            foreign_bank_user.save()

            token = Token.objects.create(
                user=foreign_bank_user,
                key="47d56c8182b60de15ef424992e52f9f2204642d1").save()

            local_bank = KnownBank.objects.create(
                user=bank_user,
                address='127.0.0.1',
                port='8000',
                name='ANFA1',
                is_local=True)

            # foreign_bank = KnownBank.objects.create(
            #     routing_number='TOP',
            #     user=foreign_bank_user,
            #     address='127.0.0.1',
            #     port='8080',
            #     name='ANFA2',
            #     is_local=False)

            central_account_ipo = Account.objects.create(
                account_type=rank,
                user_id=bank_user,
                routing_number=local_bank,
                account_name="BANK IPO Account",
                is_active=True)

            central_account_ops = Account.objects.create(
                account_type=rank,
                routing_number=local_bank,
                user_id=bank_user,
                account_name="BANK OPS Account",
                is_active=True)
            central_account_ipo.save()
            central_account_ops.save()

            Ledger.intra_transfer(
                10_000_000, central_account_ipo, "Initial amount", central_account_ops, "Initial amount", is_loan=True)

            self.create_users(central_account_ops, local_bank)

        except CommandError as e:
            print(e)

        self.stdout.write(self.style.SUCCESS('Successfully populated the Database'))

    def create_account_types(self):
        if not Account.objects.all():
            for type in AccountRanks:
                obj = AccountType.objects.create(type=type.value)
                obj.save()

    def create_users(self, ops_account, bank, account_rank: AccountRanks = AccountRanks.BASIC):
        names = ['Rafael', 'Anton', 'Mary', 'Sergei', 'Carina', 'Marcos', 'Jonathan', 'Pedro']
        last_names = ['Barbieru', 'Kamenov', 'Johnson', 'Vladistok', 'Carjila', 'Cuadrado', 'Space', 'Sánchez']
        for index, name in enumerate(names):
            first_name = name
            last_name = last_names[index]

            if index % 2 == 0:
                is_staff = True
                email = f"{first_name[0].lower()}{last_name[0].lower()}@anfa.com"
            else:
                is_staff = False
                email = f"{first_name[0].lower()}{last_name[0].lower()}@gmail.com"

            username = email

            user = User.objects.create(
                username=username,
                first_name=first_name,
                last_name=last_name,
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
                routing_number=bank,
                account_name=username,
                is_active=True)
            account.save()

            Ledger.intra_transfer(10_000, ops_account, "Initial ammount", account, "Initial ammount")
