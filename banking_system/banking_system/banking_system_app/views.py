
from .models import Account, Ledger, AccountType
from .AccountRanks import AccountRanks
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist


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
def account_info(request, account_id):
    context = {}

    if request.user.is_staff:

        account = Account.objects.filter(id=account_id)
        if account:
            account = account[0]
            owner = User.objects.filter(id=account.user_id_id)
            if owner:
                owner = owner[0]
                account_types = AccountType.objects.all()
                context = {
                    'account': account,
                    'owner': owner,
                    'account_types': account_types
                }
        return render(request, 'admin_account_details.html', context)

    account = Account.objects.get(id=account_id, is_active=True)

    can_loan = False if account.account_type.type == AccountRanks.BASIC.value else True

    context = {
        'account': account,
        'can_loan': can_loan,
    }

    return render(request, 'account_info.html', context)


@login_required(login_url='/login')
def loan(request, account_id):

    context = {}
    account = Account.objects.get(id=account_id)

    if account.account_type.type == AccountRanks.BASIC.value:
        context = {
            'error': 'This account can NOT loan money from the bank'
        }
        return render(request, 'loan.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        account.make_loan(int(amount))

    return render(request, 'loan.html', context)


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

            except (ValidationError, ObjectDoesNotExist) as e:
                context = {'error': e}
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

        active_clients_array = []
        unactive_clients_array = []
        active_clients = User.objects.filter(is_staff=False, is_active=True)
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
        return render(request, '404.html')


def show_account(request, account_id):
    account = Account.objects.filter(id=account_id)
    if account:
        account = account[0]
        owner = User.objects.filter(id=account.user_id_id)
        if owner:
            owner = owner[0]
            account_types = AccountType.objects.all()
            context = {
                'account': account,
                'owner': owner,
                'account_types': account_types
            }
    return render(request, 'admin_account_details.html', context)


def show_accounts_overview(request):
    # We make sure the user is an employee.
    if request.user.is_staff:
        active_accounts = Account.objects.filter(~Q(user_id=1), is_active=True)
        unactive_accounts = Account.objects.filter(~Q(user_id=1), is_active=False)
        context = {
            'user': request.user,
            'active_accounts': active_accounts,
            'unactive_accounts': unactive_accounts
        }
        return render(request, 'admin_accounts.html', context)
    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')


def show_employees_overview(request):
    # We make sure the user is an employee and administrator.
    if request.user.is_staff and request.user.is_superuser:
        employees = User.objects.filter(is_staff=True, is_active=True)
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


def delete_account(request, account_id, user_id):
    account_to_delete = Account.objects.filter(id=account_id)
    if (account_to_delete):
        account_to_delete = account_to_delete[0]
        account_to_delete.is_active = False
        account_to_delete.save()
    return redirect(f"/user/{ user_id }")


def delete_user(request, user_id):
    user_to_delete = User.objects.filter(id=user_id)
    if (user_to_delete):
        user_to_delete = user_to_delete[0]
        user_to_delete.is_active = False
        user_to_delete.save()
    return redirect(f"/user/{ user_id }")


def revive_user(request, user_id):
    user_to_revive = User.objects.filter(id=user_id)
    if (user_to_revive):
        user_to_revive = user_to_revive[0]
        user_to_revive.is_active = True
        user_to_revive.save()
    return redirect(f"/user/{ user_id }")


def update_account(request, account_id):
    if request.method == 'POST':
        account_to_update = Account.objects.filter(id=account_id)
        if account_to_update:
            account_to_update = account_to_update[0]
            post_data = request.POST

            # Getting the account type ID
            new_account_type_id = AccountType.objects.get(type=post_data['new_account_type'])

            account_to_update.account_type_id = new_account_type_id.id
            account_to_update.save()
    return redirect('banking_system_app:accounts')
