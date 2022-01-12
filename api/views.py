from django.http import HttpResponse


def index(request):
    raise Exception("TESTE")
    return HttpResponse("Hello, world.")