from django.contrib.auth import get_user_model
from rest_framework import serializers

from server.apps.services.serializers import ModelSerializerWithPermission
from server.apps.user.services.user import UserService

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
    income_per_hour = serializers.SerializerMethodField()

    def get_income_per_hour(self, user: User) -> int:
        """Получаем доход пользователя в час."""
        income = UserService.get_user_income_per_second(user)
        return income * 3600

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
            'referrals',
            'income_per_hour',
        )


class UserClicksSerializer(serializers.Serializer):
    """Сериалайзер для обновления баланса пользователя."""

    clicks = serializers.IntegerField(min_value=1)
