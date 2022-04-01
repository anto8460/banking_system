from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Account
from django.shortcuts import render


def home(request):

    context = {}

    if request.user:
        user = request.user
        customer= Customer.objects.get(user=user)

        if customer:
            accounts = Account.objects.filter(customer=customer)

            context = {
                'customer_name': customer.first_name,
                'customer_last_name': customer.last_name,
                'accounts': accounts,
            }

        else:
            employee = Employee.objects.filter(user=user)

        return render(request, 'home.html', context)

    if request.method == 'POST':
        ...

    # return render(request, 'index.html')

