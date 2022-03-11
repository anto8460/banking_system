from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Accounts)
admin.site.register(AccountsTransactions)
admin.site.register(AccountTypes)
admin.site.register(BankDetails)
admin.site.register(Customers)
admin.site.register(Employees)
admin.site.register(Loans)
admin.site.register(Transactions)