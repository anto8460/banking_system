from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Account)
admin.site.register(AccountsTransaction)
admin.site.register(AccountType)
admin.site.register(BankDetail)
admin.site.register(UserInformation)
admin.site.register(Loan)
admin.site.register(Transaction)
