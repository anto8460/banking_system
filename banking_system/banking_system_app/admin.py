from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Account)
admin.site.register(AccountType)
admin.site.register(UserInformation)
admin.site.register(Ledger)
admin.site.register(KnownBank)
admin.site.register(TransferRequests)
