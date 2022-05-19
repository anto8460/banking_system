from .models import Account, AccountType, Ledger
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from banking_system_app import db_utils
from django.utils import timezone


@login_required(login_url='/login')
def home(request):

    context = {}

    # If the user is already logged in.
    if request.user and not request.user.is_anonymous:
        # We assign the user from the request to a local variable.
        user = request.user
        # If the user is a customer.
        if not user.is_staff:
            accounts = Account.objects.filter(user_id=user, is_active=True).all()
            context = {'user': user, 'accounts': accounts}
            # We render the customer's homepage.
            return render(request, 'customer_home.html', context)
        # If the user is an employee
        else:
            return show_clients_overview(request)


@login_required(login_url='/login')
def clients(request):
    return show_clients_overview(request)


@login_required(login_url='/login')
def client_details(request, user_id):
    return show_user(request, user_id)


@login_required(login_url='/login')
def account_details(request, account_id):
    return show_account(request, account_id)


@login_required(login_url='/login')
def accounts(request):
    return show_accounts_overview(request)


@login_required(login_url='/login')
def employees(request):
    return show_employees_overview(request)


@login_required(login_url='/login')
def account_info(request, account_id):

    context = {}
    account = Account.objects.get(id=account_id, is_active=True)

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

        accounts = Account.objects.filter(user_id=user, is_active=True)

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
        context = get_clients_overview_response_context(request)
        return render(request, 'admin_clients.html', context)

    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')


def show_user(request, user_id):
    current_user = User.objects.filter(id=user_id)
    if (len(current_user) > 0):
        current_user = current_user[0]
        user_accounts = Account.objects.filter(user_id_id=user_id, is_active=True)
        context = {
            'current_user': current_user,
            'accounts': user_accounts
        }
        return render(request, 'admin_user_details.html', context)
    else:
        return unauth(request)


def show_account(request, account_id):
    account = Account.objects.filter(id=account_id)
    if account:
        account = account[0]
        owner = User.objects.filter(id=account.user_id_id)
        if owner:
            owner = owner[0]
            account_types = db_utils.get_account_types()
            context = {
                'account': account,
                'owner': owner,
                'account_types': account_types
            }
    return render(request, 'admin_account_details.html', context)


def show_accounts_overview(request):
    # We make sure the user is an employee.
    if request.user.is_staff:
        context = get_accounts_overview_context(request)
        return render(request, 'admin_accounts.html', context)

    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')


def show_employees_overview(request):
    # We make sure the user is an employee and administrator.
    if request.user.is_staff and request.user.is_superuser:
        employees = db_utils.get_unactive_clients()
        context = {
            'user': request.user,
            'employees': employees
        }
        return render(request, 'admin_employees.html', context)

    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')


def update_user(request, user_id):
    if request.method == 'POST':
        user_to_update = User.objects.filter(id=user_id)
        if user_to_update:
            user_to_update = user_to_update[0]
            post_data = request.POST
            user_to_update.first_name = post_data['first_name']
            user_to_update.last_name = post_data['last_name']
            user_to_update.email = post_data['email']
            user_to_update.username = post_data['email']
            user_to_update.save()
    return redirect('banking_system_app:clients')


def delete_account(request, account_id):
    if (request.user.is_staff):
        account_to_delete = Account.objects.filter(id=account_id)
        if (account_to_delete):
            account_to_delete = account_to_delete[0]
            account_to_delete.is_active = False
            account_to_delete.save()
        return redirect(f"/account/{ account_id }")
    else:
        return unauth(request)


def revive_account(request, account_id):
    if (request.user.is_staff):
        account_to_revive = Account.objects.filter(id=account_id)
        if (account_to_revive):
            account_to_revive = account_to_revive[0]
            account_to_revive.is_active = True
            account_to_revive.save()
        return redirect(f"/account/{ account_id }")
    else:
        return unauth(request)


def delete_user(request, user_id):
    if (request.user.is_staff):
        user_to_delete = User.objects.filter(id=user_id)
        if (user_to_delete):
            user_to_delete = user_to_delete[0]
            user_to_delete.is_active = False
            user_to_delete.save()
        return redirect(f"/account/{ user_id }")
    else:
        return unauth(request)


def revive_user(request, user_id):
    if (request.user.is_staff):
        user_to_revive = User.objects.filter(id=user_id)
        if (user_to_revive):
            user_to_revive = user_to_revive[0]
            user_to_revive.is_active = True
            user_to_revive.save()
        return redirect(f"/user/{ user_id }")
    else:
        return unauth(request)


def update_account(request, account_id):
    if request.method == 'POST' and request.user.is_staff:
        account_to_update = Account.objects.filter(id=account_id)
        if account_to_update:
            account_to_update = account_to_update[0]
            post_data = request.POST

            # Getting the account type ID
            new_account_type_id = AccountType.objects.get(type=post_data['new_account_type'])

            account_to_update.account_type_id = new_account_type_id.id
            account_to_update.save()
            return redirect('banking_system_app:accounts')
    else:
        return unauth()


def show_create_user(request, user_type):
    if request.user.is_staff:
        context = {
            'user_type': user_type
        }
        return render(request, 'admin_create_user.html', context)
    else:
        return unauth(request)


def create_user(request, user_type):
    if request.user.is_staff:
        post_data = request.POST
        new_user = User()
        new_user.first_name = post_data['first_name']
        new_user.last_name = post_data['last_name']
        new_user.email = post_data['email']
        new_user.username = post_data['email']
        new_user.is_staff = user_type == 'employee'
        new_user.is_active = False
        new_user.set_password('12345678')
        new_user.save()
        if user_type == 'client':
            context = get_clients_overview_response_context(request)
            return render(request, 'admin_clients.html', context)
        elif user_type == 'employee':
            return render(request, 'admin_employees.html')
    else:
        return unauth(request)


def get_clients_overview_response_context(request):
    active_clients_array = []
    unactive_clients_array = []
    active_clients = db_utils.get_active_clients()
    unactive_clients = User.objects.filter(is_staff=False, is_active=False)

    for client in active_clients:
        number_of_accounts = Account.objects.filter(
            user_id=client.id, is_active=True).count()

        active_clients_array.append({
            'details': client,
            'number_of_accounts': number_of_accounts
        })

    for client in unactive_clients:
        number_of_accounts = Account.objects.filter(
            user_id=client.id, is_active=True).count()

        unactive_clients_array.append({
            'details': client,
            'number_of_accounts': number_of_accounts
        })

    context = {
        'user': request.user,
        'active_clients': active_clients_array,
        'unactive_clients': unactive_clients_array
    }

    return context


def get_accounts_overview_context(request):
    active_accounts = db_utils.get_active_accounts()
    unactive_accounts = db_utils.get_unactive_accounts()

    active_accounts_array = []
    unactive_accounts_array = []

    for account in active_accounts:
        owner = User.objects.get(id=account.user_id_id)
        active_accounts_array.append({
            'details': account,
            'owner': owner
        })

    for account in unactive_accounts:
        owner = User.objects.get(id=account.user_id_id)
        unactive_accounts_array.append({
            'details': account,
            'owner': owner
        })

    return {
        'user': request.user,
        'active_accounts': active_accounts_array,
        'unactive_accounts': unactive_accounts_array
    }


def show_create_account(request):
    if (request.user.is_staff):
        account_types = db_utils.get_account_types()
        clients = db_utils.get_active_clients()
        context = {
            'account_types': account_types,
            'clients': clients
        }
        return render(request, 'admin_create_account.html', context)
    else:
        return unauth(request)


def create_account(request):
    if (request.user.is_staff):
        post_data = request.POST
        account_type = post_data['account_type']
        account_owner = User.objects.get(id=post_data['account_owner'])
        new_account = Account(
            account_name=account_owner.email,
            created_at=timezone.now(),
            account_type_id=account_type,
            user_id_id=account_owner.id,
            is_active=False
        )
        new_account.save()
        context = get_accounts_overview_context(request)
        return render(request, 'admin_accounts.html', context)
    else:
        return unauth(request)


def unauth(request):
    return render(request, '404.html')
