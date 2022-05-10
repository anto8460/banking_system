from multiprocessing.dummy.connection import Client
from django.http import HttpResponse
from .models import Account, Ledger
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
            accounts = Account.objects.filter(user_id=user).all()

            context = {
                'user': user,
                'accounts': accounts
            accounts = Account.objects.filter(user_id=user)

            context = {
                'user': user,
                'accounts': accounts,
            }

            # We render the customer's homepage.
            return render(request, 'customer_home.html', context)

        # If the user is an employee
        else:            
            clients_array = []
            clients = User.objects.filter(is_staff = False)[:5]
            for client in clients:
                number_of_accounts = Account.objects.filter(user_id=client.id).count()
                clients_array.append(
                    {
                        'details': client, 
                        'number_of_accounts': number_of_accounts
                    }
                )
                
            accounts_array = [] 
            accounts = Account.objects.all()[:5]
            for account in accounts:
                account_user = User.objects.filter(id=account.user_id.id).get()
                accounts_array.append(
                    {
                        'details': account,
                        'user': account_user
                    }
                )
                
            context = {
                'user': user,
                'clients': clients_array,
                'accounts': accounts_array
            }
            
            # We render the employee's homepage.
            return render(request, 'employee_home.html', context)

@login_required(login_url='/clients')
def clients(request):
    if request.user.is_staff:
        return render(request, 'clients.html')
    else:
        # We render an authorization error
        return render(request, 'auth_error.html')
        return render(request, 'customer_home.html', context)


@login_required(login_url='/login')
def account_info(request, account_id):

    context = {}
    account = Account.objects.get(id=account_id)

    context = {
        'account': account,
    }

    return render(request, 'account_info.html', context)


@login_required(login_url='/login')
def transfer(request):

    context = {}

    if request.user and not request.user.is_anonymous:

        user = request.user

        accounts = Account.objects.filter(user_id=user)

        context = {
            'accounts': accounts,
        }

        if request.method == 'POST':
            print(request.POST['recipient'])
            print(request.POST['amount'])
            print(request.POST['account_id'])


            debit = Account.objects.get(id="c22f394d-0bea-465a-9b36-0ff92dee06c8")
            credit = Account.objects.get(id="6c2438a6-4d08-4db8-9440-bbfd84c42d96")

            Ledger.transfer(10_000, credit, "Salary", debit, "Initial transfer",)

            return render(request, 'transfer_form.html', context)
        else:
            return render(request, 'transfer_form.html', context)
