from django.http import HttpResponse
from rest_framework.generics import CreateAPIView

from .models import Account
from .serializers import AccountSerializer


def index(request):
    return HttpResponse("Hello, world.")


class CreateAccountView(CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
