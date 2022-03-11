from django.http import HttpResponse
from django.shortcuts import render


def home(request):

    contex = {}

    if request.method == 'POST':
        ...

    return HttpResponse('You are logged in')
    # return render(request, 'index.html')

