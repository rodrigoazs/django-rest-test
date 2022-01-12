from django.contrib.auth.models import User
from django.db import transaction
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountBalanceSerializer, AmountSerializer, UserSerializer


def index(request):
    return HttpResponse("Hello, world.")


class AccountCreateView(APIView):
    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        if user_serializer.is_valid():
            password = user_serializer.validated_data.get("password")
            user = User.objects.create(**user_serializer.validated_data)
            user.set_password(password)
            user.save()
            account = Account.objects.create(user=user)
            account.save()
            response = {
                "date_created": account.date_created,
                "is_active": account.is_active,
                "balance": account.balance,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
            }

            return Response({"message": "account created", "data": response}, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountBalanceView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk):
        user = request.user
        account = Account.objects.get(pk=pk)
        if user == account.user:
            serializer = AccountBalanceSerializer(account)
            return Response(serializer.data)
        return Response({"message": "not allowed"}, status=status.HTTP_400_BAD_REQUEST)


class DepositView(APIView):
    def put(self, request, pk):
        serializer = AmountSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                account = Account.objects.get(pk=pk)
                account.balance += serializer.validated_data.get("amount", 0.0)
                account.save()
                return Response(
                    {"message": "deposit made", "new_balance": account.balance}, status=status.HTTP_201_CREATED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Withdrawal(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request, pk):
        user = request.user
        serializer = AmountSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                account = Account.objects.get(pk=pk)
                if user == account.user:
                    amount = serializer.validated_data.get("amount", 0.0)
                    if account.balance >= amount:
                        account.balance -= amount
                        account.save()
                        return Response(
                            {"message": "withdrawal made", "balance": account.balance}, status=status.HTTP_201_CREATED
                        )
                    else:
                        return Response(
                            {"message": "insufficient balance", "balance": account.balance},
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                else:
                    return Response({"message": "not allowed"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
