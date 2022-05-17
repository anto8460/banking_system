from django.shortcuts import render, reverse
from django.contrib.auth import authenticate, login as dj_login, logout as dj_logout
from django.shortcuts import HttpResponseRedirect
from .MFA import MFA_Task
from banking_system_app.models import UserInformation
from .Utils.generate_code import generate_code


def login(request):

    context = {}
    if request.method == 'POST':
        user = authenticate(request, username=request.POST['user'], password=request.POST['password'])
        if user:
            user_info = UserInformation.objects.get(user=user.id)

            if user_info.use_mfa:
                code = generate_code()
                request.session['code'] = code
                request.session['user'] = request.POST['user']
                request.session['password'] = request.POST['password']
                phone_number = user_info.phone_number

                MFA_Task.send_code(code, phone_number)

                return HttpResponseRedirect(reverse('login_app:verify_code'))

            else:
                dj_login(request, user)
                return HttpResponseRedirect(reverse('banking_system_app:home'))

        else:
            context = {
                'error': 'Wrong username or password!'
            }

    return render(request, 'login.html', context)


def verify_code(request):

    context = {}

    if request.method == 'POST':
        if request.POST['code'] == request.session['code']:
            user = authenticate(
                request,
                username=request.session['user'],
                password=request.session['password'])
            dj_login(request, user)
            return HttpResponseRedirect(reverse('banking_system_app:home'))
        else:
            context = {
                'error': 'Wrong Code entered, Please try again'
            }

    return render(request, 'verify_code.html', context)


def logout(request):
    dj_logout(request)
    return render(request, 'login.html')


# TODO
def password_reset(request):
    ...


# TODO
def sign_up(request):
    ...
