from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountBalanceSerializer, AccountSerializer, AmountSerializer


def index(request):
    return HttpResponse("Hello, world.")


class AccountCreateView(APIView):
    def post(self, request):
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            password = serializer.validated_data.get("password")
            user = User.objects.create(
                username=serializer.validated_data.get("username"),
                first_name=serializer.validated_data.get("first_name"),
                last_name=serializer.validated_data.get("last_name"),
                email=serializer.validated_data.get("email"),
            )
            user.set_password(password)
            user.save()
            account = Account.objects.create(
                date_created=serializer.validated_data.get("date_created"),
                is_active=serializer.validated_data.get("is_active"),
                balance=serializer.validated_data.get("balance"),
                user=user,
            )
            account.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountBalanceView(APIView):
    def get(self, request, pk):
        account = Account.objects.all().get(pk=pk)
        serializer = AccountBalanceSerializer(account)
        return Response(serializer.data)


class DepositView(APIView):
    def put(self, request, pk):
        serializer = AmountSerializer(data=request.data)
        if serializer.is_valid():
            account = Account.objects.get(pk=pk)
            account.balance += serializer.validated_data.get("amount", 0.0)
            account.save()
            return Response({"message": "deposit made", "new_balance": account.balance}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Withdrawl(APIView):
    def put(self, request, pk):
        serializer = AmountSerializer(data=request.data)
        if serializer.is_valid():
            account = Account.objects.get(pk=pk)
            amount = serializer.validated_data.get("amount", 0.0)
            if account.balance >= amount:
                account.balance -= amount
                account.save()
                return Response(
                    {"message": "withdrawl made", "balance": account.balance}, status=status.HTTP_201_CREATED
                )
            else:
                return Response(
                    {"message": "insufficient balance", "balance": account.balance}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
