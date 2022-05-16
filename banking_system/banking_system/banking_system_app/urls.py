from django.urls import path

from . import views

app_name = 'banking_system_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('clients', views.show_clients_overview, name='show_clients_overview'),
    path('user/<user_id>', views.show_user, name='show_user'),
    path('delete_user/<user_id>', views.delete_user, name='delete_user'),
    path('revive_user/<user_id>', views.revive_user, name='revive_user'),
    path('account/<account_id>', views.account_info, name='account_details'),
    path('accounts', views.show_accounts_overview, name='show_accounts_overview'),
    path('update_account/<account_id>', views.update_account, name='update_account'),
    path('employees', views.show_employees_overview, name='show_employees_overview'),
    path('transfer', views.transfer, name='transfer'),
    path('account/<account_id>', views.account_info, name='account_info'),
    path('loan/<account_id>', views.loan, name='loan'),
    path('update_user/<user_id>', views.update_user, name='update_user'),
    path('delete_account/<account_id>/<user_id>', views.delete_account, name='delete_account'),
]
