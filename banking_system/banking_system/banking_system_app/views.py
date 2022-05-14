from .models import Account, Ledger
from django.db.models import Q
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


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
            context = {'user': user, 'accounts': accounts}
            # We render the customer's homepage.
            return render(request, 'customer_home.html', context)
        # If the user is an employee
        else:
            return show_clients_overview(request)


@login_required(login_url='/clients')
def clients(request):
    return show_clients_overview(request)
    
@login_required(login_url='/login')
def accounts(request):
    return show_accounts_overview(request)


@login_required(login_url='/login')
def account_info(request, account_id):

    context = {}
    account = Account.objects.get(id=account_id)

    context = {
        'account': account,
    }
    print(account.movements[0])

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
            try:
                sender = Account.objects.get(id=request.POST['sender'])
                recipient = Account.objects.get(id=request.POST['recipient'])

                if sender == recipient:
                    raise ValidationError(
                        "Recipient account number is the same as the sender")

            except ValidationError as e:
                context = {'error': e.message}
                return render(request, 'transfer_form.html', context)

            amount = request.POST['amount']
            text = request.POST['text']

            # Make transaction
            Ledger.transfer(float(amount), sender, text, recipient, text)

            context['success'] = 'true'

            return render(request, 'transfer_form.html', context)
        else:
            return render(request, 'transfer_form.html', context)

def show_clients_overview(request):
    # We make sure the user is an employee.
    if request.user.is_staff:
        
        clients_array = []
        clients = User.objects.filter(is_staff=False)
        
        for client in clients:
            number_of_accounts = Account.objects.filter(
                user_id=client.id).count()
            clients_array.append({
                'details': client,
                'number_of_accounts': number_of_accounts
            })
           
            context = {
                'user': request.user,
                'clients': clients_array
            }
            
        return render(request, 'clients.html', context)           
            
    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')
    
def show_accounts_overview(request):
    # We make sure the user is an employee.
    if request.user.is_staff:
        accounts = Account.objects.filter(~Q(user_id=1))           
        context = {
            'user': request.user,
            'accounts': accounts
        }            
        return render(request, 'accounts.html', context)           
            
    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')