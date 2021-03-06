
from django.http import HttpResponseRedirect
from .models import Account, AccountType, Ledger, UserInformation, KnownBank, TransferRequests
from .AccountRanks import AccountRanks
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from banking_system_app import db_utils, sms_task
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
            return render(request, 'client/customer_home.html', context)
        # If the user is an employee
        else:
            return show_clients_overview(request)


@login_required(login_url='/login')
def transfer_requests(request, account_id):

    tr_requests = TransferRequests.objects.filter(to_account=account_id)
    my_requests = TransferRequests.objects.filter(from_account=account_id)
    account = Account.objects.get(id=account_id)

    context = {
        'requests': tr_requests,
        'my_requests': my_requests,
        'account': account,
    }

    return render(request, 'client/transfer_requests.html', context)


@login_required(login_url='/login')
def request_details(request, request_id):
    tr_request = TransferRequests.objects.get(id=request_id)
    user = request.user
    user_accounts = Account.objects.filter(user_id=user)

    is_mine = True if tr_request.from_account in user_accounts else False

    context = {
        'tr_request': tr_request,
        'is_mine': is_mine,
    }

    tr_request.is_new = False
    tr_request.save()

    if request.method == 'POST':
        if 'pay' in request.POST:
            if not is_mine:
                text = "Transaction Request: " + tr_request.text
                Ledger.intra_transfer(
                    amount=tr_request.amount,
                    debit_account=tr_request.to_account,
                    debit_text=text,
                    credit_account=tr_request.from_account,
                    credit_text=text)

                tr_request.delete()
        elif 'close' in request.POST:
            tr_request.is_closed = True
            tr_request.save()

        elif 'open' in request.POST:
            tr_request.is_closed = False
            tr_request.save()

    return render(request, 'client/request_details.html', context)


@login_required(login_url='/login')
def make_request(request):

    user = request.user
    accounts = Account.objects.filter(user_id=user)

    context = {
        'user': user,
        'accounts': accounts,
    }

    if request.method == 'POST':
        try:
            from_account = request.POST['from_account']
            to_account = request.POST['to_account']

            if from_account == to_account:
                raise ValidationError

            from_account = Account.objects.get(id=from_account)
            to_account = Account.objects.get(id=to_account)

            amount = float(request.POST['amount'])
            text = request.POST['text']

            tr_request = TransferRequests.objects.create(
                from_account=from_account,
                to_account=to_account,
                amount=amount,
                text=text)

            tr_request.save()

            return HttpResponseRedirect(f"/transfer_requests/{from_account.id}")

        except (ValidationError, ObjectDoesNotExist) as e:
            context = {'error': e}
            return render(request, 'client/make_request.html', context)

    return render(request, 'client/make_request.html', context)


@login_required(login_url='/login')
def user_profile(request):
    user = request.user
    user_info = UserInformation.objects.get(user=user)
    context = {
        'user': user,
        'info': user_info
    }
    if request.method == 'POST':
        user_info.phone_number = request.POST['phone']

        user_info.use_mfa = True if 'use_mfa' in request.POST else False
        user_info.save()

    return render(request, 'client/user_profile.html', context)


@login_required(login_url='/login')
def account_details(request, account_id):
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
        return render(request, 'admin/admin_account_details.html', context)

    account = Account.objects.get(id=account_id, is_active=True)

    can_loan = False if account.account_type.type == AccountRanks.BASIC.value else True

    context = {
        'account': account,
        'can_loan': can_loan,
    }

    return render(request, 'client/account_details.html', context)


@login_required(login_url='/login')
def loan(request, account_id):

    context = {}
    account = Account.objects.get(id=account_id)

    if account.account_type.type == AccountRanks.BASIC.value:
        context = {
            'error': 'This account can NOT loan money from the bank'
        }
        return render(request, 'client/loan.html', context)

    if request.method == 'POST':
        amount = request.POST['amount']

        account.make_loan(float(amount))

    return render(request, 'client/loan.html', context)


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

            routing_number = request.POST['recipient'][:3]
            account_id = request.POST['recipient'][3:]

            try:
                known_bank = KnownBank.objects.filter(routing_number=routing_number)

                if not known_bank:
                    raise ObjectDoesNotExist('Unknown routing number')

                if known_bank[0].is_local:

                    sender = Account.objects.get(id=request.POST['sender'])
                    recipient = Account.objects.get(id=account_id)

                    amount = request.POST['amount']
                    text = request.POST['text']

                    if sender == recipient:
                        raise ValidationError(
                            "Recipient account number is the same as the sender")

                    # Make transaction
                    Ledger.intra_transfer(float(amount), sender, text, recipient, text)

                    context['status'] = 'true'

                    # Sending SMS confirmation to both parties
                    sender_owner = UserInformation.objects.get(user=sender.user_id_id)
                    recipient_owner = UserInformation.objects.get(user=recipient.user_id_id)
                    sender_message = f"Hi! You just sent { amount } DKK to { recipient.id }"
                    recipient_message = f"Hi! You have been transferred { amount } DKK to { recipient.id }"
                    sms_task.send_message(sender_message, sender_owner.phone_number)
                    sms_task.send_message(recipient_message, recipient_owner.phone_number)

                else:
                    sender = Account.objects.get(id=request.POST['sender'])
                    recipient = account_id
                    amount = float(request.POST['amount'])
                    text = request.POST['text']

                    success = Ledger.inter_transfer(amount, sender, text, recipient, known_bank[0])

                    context['status'] = 1 if success else 0

                return HttpResponseRedirect(f"/account/{request.POST['sender']}")

            except (ValidationError, ObjectDoesNotExist) as e:
                context = {'error': e}
                return render(request, 'client/transfer_form.html', context)

        else:
            return render(request, 'client/transfer_form.html', context)


@login_required(login_url='/login')
def show_clients_overview(request):
    # We make sure the user is an employee.
    if request.user.is_staff:
        context = get_clients_overview_response_context(request)
        return render(request, 'admin/admin_clients.html', context)

    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')


@login_required(login_url='/login')
def show_user(request, user_id):
    current_user = User.objects.filter(id=user_id)
    if (len(current_user) > 0):
        current_user = current_user[0]
        user_accounts = Account.objects.filter(user_id_id=user_id, is_active=True)
        user_info = UserInformation.objects.get(user_id=current_user)

        context = {
            'current_user': current_user,
            'accounts': user_accounts,
            'user_info': user_info,
            'date': user_info.date_of_birth.strftime('%Y-%m-%d'),
        }
        return render(request, 'admin/admin_user_details.html', context)
    else:
        return unauth(request)


@login_required(login_url='/login')
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
    return render(request, 'admin/admin_account_details.html', context)


@login_required(login_url='/login')
def show_accounts_overview(request):
    # We make sure the user is an employee.
    if request.user.is_staff:
        context = get_accounts_overview_context(request)
        return render(request, 'admin/admin_accounts.html', context)

    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')


@login_required(login_url='/login')
def show_employees_overview(request):
    # We make sure the user is an employee and administrator.
    if request.user.is_staff and request.user.is_superuser:
        context = get_employees_overview_response_context(request)
        return render(request, 'admin/admin_employees.html', context)

    else:
        # If the user is not an employee, we render an authorization error
        return render(request, 'auth_error.html')


@login_required(login_url='/login')
def update_user(request, user_id):
    if request.method == 'POST':
        user_to_update = User.objects.filter(id=user_id)
        info_to_update = UserInformation.objects.get(user=user_to_update[0])
        if user_to_update:
            user_to_update = user_to_update[0]
            post_data = request.POST
            user_to_update.first_name = post_data['first_name']
            user_to_update.last_name = post_data['last_name']
            user_to_update.email = post_data['email']
            user_to_update.username = post_data['email']
            user_to_update.save()

            info_to_update.date_of_birth = post_data['date']
            info_to_update.cpr = post_data['cpr']
            info_to_update.phone_number = post_data['phone']
            info_to_update.save()

    return redirect('banking_system_app:clients')


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def delete_user(request, user_id):
    if (request.user.is_staff):
        user_to_delete = User.objects.filter(id=user_id)
        if (user_to_delete):
            user_to_delete = user_to_delete[0]
            user_to_delete.is_active = False
            user_to_delete.save()
        return redirect(f"/user/{ user_id }")
    else:
        return unauth(request)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def show_create_user(request, user_type):
    if request.user.is_staff:
        context = {
            'user_type': user_type
        }
        return render(request, 'admin/admin_create_user.html', context)
    else:
        return unauth(request)


@login_required(login_url='/login')
def create_user(request, user_type):
    if request.user.is_staff:
        post_data = request.POST
        new_user = User()
        new_user.first_name = post_data['first_name']
        new_user.last_name = post_data['last_name']
        new_user.email = post_data['email']
        new_user.username = post_data['email']
        new_user.is_staff = user_type == 'employee'
        if user_type == 'client':
            new_user.is_active = False
        elif user_type == 'employee':
            new_user.is_active = True
        new_user.set_password('12345678')
        new_user.save()

        user_info = UserInformation.objects.create(
            user=new_user,
            date_of_birth=post_data['date'],
            cpr=post_data['cpr'],
            phone_number=post_data['phone'],
        )
        user_info.save()

        if user_type == 'client':
            context = get_clients_overview_response_context(request)
            return render(request, 'admin/admin_clients.html', context)
        elif user_type == 'employee':
            context = get_employees_overview_response_context(request)
            return render(request, 'admin/admin_employees.html', context)
    else:
        return unauth(request)


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def get_employees_overview_response_context(request):
    active_employees = db_utils.get_active_employees()
    unactive_employees = db_utils.get_unactive_employees()
    return {
        'user': request.user,
        'active_employees': active_employees,
        'unactive_employees': unactive_employees
    }


@login_required(login_url='/login')
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


@login_required(login_url='/login')
def show_create_account(request):
    if (request.user.is_staff):
        account_types = db_utils.get_account_types()
        clients = db_utils.get_active_clients()
        context = {
            'account_types': account_types,
            'clients': clients
        }
        return render(request, 'admin/admin_create_account.html', context)
    else:
        return unauth(request)


@login_required(login_url='/login')
def create_account(request):
    if (request.user.is_staff):
        post_data = request.POST
        account_type = post_data['account_type']
        account_owner = User.objects.get(id=post_data['account_owner'])
        local_routing_number = KnownBank.objects.get(routing_number='ARF')
        new_account = Account(
            account_name=account_owner.email,
            created_at=timezone.now(),
            account_type_id=account_type,
            user_id_id=account_owner.id,
            is_active=False,
            routing_number = local_routing_number
        )
        new_account.save()
        context = get_accounts_overview_context(request)
        return render(request, 'admin/admin_accounts.html', context)
    else:
        return unauth(request)


@login_required(login_url='/login')
def unauth(request):
    return render(request, '404.html')
