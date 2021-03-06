from django.urls import path
from . import views

app_name = 'login_app'

urlpatterns = [
    path('', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    path('verify_code', views.verify_code, name='verify_code'),
]
