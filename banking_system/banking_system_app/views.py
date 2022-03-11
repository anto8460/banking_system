from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Customer, Employee, Account
from django.shortcuts import render


def home(request):

    contex = {}

    if request.user:
        user = request.user
        customer = Customer.objects.filter(user=user)

        if customer:
            # accounts = Account.filter.get(customer=customer)
            # print(accounts)
            ...
        else:
            employee = Employee.objects.filter(user=user)
        return HttpResponse('You are logged with ')

    if request.method == 'POST':
        ...

    # return render(request, 'index.html')

