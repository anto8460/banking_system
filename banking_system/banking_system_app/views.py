from django.http import HttpResponse


def index(request):
    return HttpResponse("If you are seeing this, the banking system is working!")

