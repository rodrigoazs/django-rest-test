from django.conf import settings
from django.contrib.auth.models import User
from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Account
from .serializers import AccountBalanceSerializer, AmountSerializer, UserSerializer


class AccountCreateView(APIView):
    """A view for creating a bank account. An account is associated to an user."""

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)

        # validate serialization
        if user_serializer.is_valid():
            # create user
            password = user_serializer.validated_data.get("password")
            user = User.objects.create(**user_serializer.validated_data)
            user.set_password(password)
            user.save()

            # create account associated to user
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

            return Response(response, status=status.HTTP_201_CREATED)
        return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AccountBalanceView(APIView):
    """A view for checking person own account balance.
    Need authentication.
    """

    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        # get authenticated user account
        account = Account.objects.get(user=user)
        serializer = AccountBalanceSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


class DepositView(APIView):
    """A view for depositing money in someones' account."""

    def put(self, request, username):
        serializer = AmountSerializer(data=request.data)

        # validate serialization
        if serializer.is_valid():
            with transaction.atomic():
                # get user account to deposit
                account = Account.objects.filter(user__username=username).first()

                # if account was not found
                if account is None:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                # deposit money
                account.balance += serializer.validated_data.get("amount", 0.0)

                # check if user balance is maximum after depositing
                if account.balance > settings.MAX_BALANCE_AMOUNT:
                    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)

                # save deposit
                account.save()

                return Response({"balance": account.balance}, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class WithdrawalView(APIView):
    """A view for withdrawing money from person own account.
    Need authentication.
    """

    permission_classes = (IsAuthenticated,)

    def put(self, request):
        user = request.user
        serializer = AmountSerializer(data=request.data)

        # validate serialization
        if serializer.is_valid():
            with transaction.atomic():
                # get authenticated user account
                account = Account.objects.get(user=user)
                # get amount to withdraw
                amount = serializer.validated_data.get("amount", 0.0)

                # check if user has enough money
                if account.balance >= amount:
                    # withdraw money
                    account.balance -= amount
                    account.save()
                    return Response({"balance": account.balance}, status=status.HTTP_202_ACCEPTED)
                else:
                    return Response(
                        {"balance": account.balance},
                        status=status.HTTP_406_NOT_ACCEPTABLE,
                    )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
