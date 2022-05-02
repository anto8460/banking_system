from django.http import HttpResponse
from .models import Account
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login')
def home(request):

    context = {}

    # If the user is already logged in.
    if request.user and not request.user.is_anonymous:

        # We assign the user from the request to a local variable.
        user = request.user

        # If the user is a customer.
        if not user.is_staff:
            accounts = Account.objects.filter(user_id=user)
            print(accounts[0].get_balance())
            context = {
                'user': user,
                'accounts': accounts
            }

            # We render the customer's homepage.
            return render(request, 'customer_home.html', context)

        # If the user is an employee
        else:
            context = {}

        return render(request, 'home.html', context)
