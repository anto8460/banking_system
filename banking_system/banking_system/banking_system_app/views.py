from django.http import HttpResponse
from .models import Account, UserInformation
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
            account = Account.objects.get(user_id=user)

            context = {
                'user': user,
                'account': account,
                'balance': account.get_balance(),
                'transactions': account.get_transactions()
            }

            # We render the customer's homepage.
            return render(request, 'customer_home.html', context)

        # If the user is an employee
        else:
            clients = [
                {
                'first_name': 'Alberto',
                'last_name': 'Unamuno',
                'email': 'minecraft@gmail.com',
                'number_of_accounts': 5,
                },
                {
                'first_name': 'Caca',
                'last_name': 'Entuboca',
                'email': 'cacaentuboca@gmail.com',
                'number_of_accounts': 5,
                },
                {
                'first_name': 'rafa',
                'last_name': 'eeeeeeee',
                'email': 'mimimimi@gmail.com',
                'number_of_accounts': 5,
                },
                {
                'first_name': 'Minecraft',
                'last_name': 'Unamuno',
                'email': 'alberto_unamuno@gmail.com',
                'number_of_accounts': 5,
                },
                {
                'first_name': 'Alberto',
                'last_name': 'Unamuno',
                'email': 'alberto_unamuno@gmail.com',
                'number_of_accounts': 5,
                },
                {
                'first_name': 'Alberto',
                'last_name': 'Unamuno',
                'email': 'alberto_unamuno@gmail.com',
                'number_of_accounts': 5,
                },
                {
                'first_name': 'Alberto',
                'last_name': 'Unamuno',
                'email': 'alberto_unamuno@gmail.com',
                'number_of_accounts': 5,
                }
            ]
            context = {
                'user': user,
                'clients': clients
            }
            
            # We render the employee's homepage.
            return render(request, 'employee_home.html', context)
