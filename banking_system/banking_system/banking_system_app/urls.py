from django.urls import path

from . import views

app_name = 'banking_system_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('clients', views.clients, name='clients'),
    path('user/<user_id>', views.client_details, name='user_details'),
    path('account/<account_id>', views.account_details, name='account_details'),
    path('accounts', views.accounts, name='accounts'),
    path('employees', views.employees, name='employees'),    
    path('transfer', views.transfer, name='transfer'),
    path('account/<account_id>', views.account_info, name='account_info'),
]
