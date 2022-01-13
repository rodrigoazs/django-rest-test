from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    """Serializer for user model"""

    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


class AccountBalanceSerializer(serializers.Serializer):
    """Serializer for account balance"""

    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.0)


class AmountSerializer(serializers.Serializer):
    """Serializer for deposit/withdrawal request"""

    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.0)
