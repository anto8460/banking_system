from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Account
from django.shortcuts import render


def home(request):

    context = {}

    if request.user:
        user = request.user

        if not user.is_staff:
            accounts = Account.objects.filter(user_id=user)

            context = {
                'customer_name': user.first_name,
                'customer_last_name': user.last_name,
                'accounts': accounts,
            }

        else:
            context = {}
        return render(request, 'home.html', context)

    if request.method == 'POST':
        ...

    # return render(request, 'index.html')

