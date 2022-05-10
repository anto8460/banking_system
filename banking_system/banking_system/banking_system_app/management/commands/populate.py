import secrets
from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from banking_system_app.models import Account, Ledger


class Command(BaseCommand):
    help = 'Populates the database with a central account and 2 users'

    def handle(self):

        try:
            bank_user = User.objects.create_user('bank', email='', password=secrets.token_urlsafe(64))
            bank_user.is_active = False
            bank_user.save()

            central_account = Account.objects.create()
        except CommandError as e:
            print(e)

        self.stdout.write(self.style.SUCCESS('Successfully closed poll "%s"' % poll_id))