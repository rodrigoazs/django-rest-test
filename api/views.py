import datetime

from django.contrib.auth.models import User
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import (
    AccountBalanceSerializer,
    AccountSerializer,
    AmountSerializer,
    UserSerializer,
)


def index(request):
    return HttpResponse("Hello, world.")


class AccountCreateView(APIView):
    def post(self, request):
        account_serializer = AccountSerializer(data=request.data)
        user_seriallizer = UserSerializer(data=request.data)
        if account_serializer.is_valid() and user_seriallizer.is_valid():
            password = user_seriallizer.validated_data.get("password")
            user = User.objects.create(**user_seriallizer.validated_data)
            user.set_password(password)
            user.save()
            account = Account.objects.create(
                **account_serializer.validated_data,
                date_created=datetime.datetime.now(),
                user=user,
            )
            account.save()
            return Response(account_serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            {"account": account_serializer.errors, "user": user_seriallizer.errors}, status=status.HTTP_400_BAD_REQUEST
        )


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
