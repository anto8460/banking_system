from django.urls import path

from banking_system_app import views

app_name = 'banking_system_app'

urlpatterns = [

    # ========== Template endpoints ==========

    # Home
    path('', views.home, name='home'),

    # Clients
    path('clients', views.show_clients_overview, name='clients'),

    # Employees
    path('employees', views.show_employees_overview, name='employees'),

    # Users
    path('user/<user_id>', views.show_user, name='user_details'),
    path('show_create_user/<user_type>', views.show_create_user, name='show_create_user'),

    # Accounts
    path('accounts', views.show_accounts_overview, name='accounts'),
    path('show_create_account', views.show_create_account, name='show_create_account'),
    path('account/<account_id>', views.account_details, name='account_details'),

    # Loan
    path('loan/<account_id>', views.loan, name='loan'),

    # User profile
    path('profile', views.user_profile, name='user_profile'),

    # Transfer Requests
    path('transfer_requests/<account_id>', views.transfer_requests, name='transfer_request'),
    path('request/<request_id>', views.request_details, name='request_details'),
    path('make_request/', views.make_request, name='make_request'),


    # ========== Action endpoints ==========

    # User
    path('create_user/<user_type>', views.create_user, name='create_user'),
    path('update_user/<user_id>', views.update_user, name='update_user'),
    path('delete_user/<user_id>', views.delete_user, name='delete_user'),
    path('revive_user/<user_id>', views.revive_user, name='revive_user'),

    # Account
    path('create_account', views.create_account, name='create_account'),
    path('update_account/<account_id>', views.update_account, name='update_account'),
    path('delete_account/<account_id>', views.delete_account, name='delete_account'),
    path('delete_account/<account_id>/<user_id>', views.delete_account, name='delete_account'),
    path('revive_account/<account_id>', views.revive_account, name='revive_account'),

    # Others
    path('transfer', views.transfer, name='transfer'),
]
