# from django.http import HttpResponse
from django.shortcuts import render, reverse
# from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.shortcuts import HttpResponseRedirect
# from banking_system.banking_system_app.models import Customers, Accounts


def login(request):
    context = {}
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user:
            dj_login(request, user)
            return HttpResponseRedirect(reverse('banking_system_app:home'))
        else:
            context = {
                'error': 'Wrong username or password!'
            }

    return render(request, 'login.html', context)


def logout(request):
    dj_logout(request)
    return render(request, 'login.html')


# TODO
def password_reset(request):
    ...


# TODO
def sign_up(request):
    ...
