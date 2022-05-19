from django.urls import path

from . import views

app_name = 'banking_system_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('clients', views.clients, name='clients'),
    path('show_create_user/<user_type>', views.show_create_user, name='show_create_user'),
    path('create_user/<user_type>', views.create_user, name='create_user'),    
    path('user/<user_id>', views.client_details, name='user_details'),
    path('delete_user/<user_id>', views.delete_user, name='delete_user'),
    path('revive_user/<user_id>', views.revive_user, name='revive_user'),
    path('delete_account/<account_id>', views.delete_account, name='delete_account'),
    path('revive_account/<account_id>', views.revive_account, name='revive_account'),
    path('account/<account_id>', views.account_details, name='account_details'),
    path('accounts', views.accounts, name='accounts'),
    path('update_account/<account_id>', views.update_account, name='update_account'),
    path('employees', views.employees, name='employees'),
    path('transfer', views.transfer, name='transfer'),
    path('account/<account_id>', views.account_info, name='account_info'),
    path('update_user/<user_id>', views.update_user, name='update_user'),
    path('delete_account/<account_id>/<user_id>', views.delete_account, name='delete_account'),
    path('show_create_account', views.show_create_account, name='show_create_account'),
    path('create_account', views.create_account, name='create_account')
]
