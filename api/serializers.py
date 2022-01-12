from rest_framework import serializers


class AccountSerializer(serializers.Serializer):
    date_created = serializers.DateField()
    is_active = serializers.BooleanField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.CharField()
    password = serializers.CharField()


class AccountBalanceSerializer(serializers.Serializer):
    balance = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.0)


class AmountSerializer(serializers.Serializer):
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, default=0.0)
