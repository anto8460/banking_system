from django.urls import path, include
from .api import HasAccount, CreateTransaction

app_name = 'banking_system_api'

urlpatterns = [
    path('v1/dj-rest-auth/', include('dj_rest_auth.urls')),
    path('v1/account/<str:pk>', HasAccount.as_view()),
    path('v1/inter-transaction', CreateTransaction.as_view())
]
