from django.urls import path

from . import views

app_name = 'banking_system_app'

urlpatterns = [
    path('', views.home, name='home'),
    path('clients', views.clients, name='clients')
    path('transfer', views.transfer, name='transfer'),
    path('account/<account_id>', views.account_info, name='account_info'),
]
