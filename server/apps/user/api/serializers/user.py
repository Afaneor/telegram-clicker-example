from django.contrib.auth import get_user_model
from rest_framework import serializers

from server.apps.services.serializers import ModelSerializerWithPermission

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    """Сериалайзер пользователя. Используется в других сериалайзерах."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'last_claimed',
            'last_balance_update',
            'balance',
        )


class UserSerializer(ModelSerializerWithPermission):
    """Детальная информация о пользователе."""

    referrals = BaseUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'last_claimed',
            'last_balance_update',
            'balance',
        )
