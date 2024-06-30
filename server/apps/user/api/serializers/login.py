from typing import Optional

from django.contrib.auth import authenticate
from rest_framework import serializers

from server.apps.user.models import User
from server.apps.user.services.check_user import check_django_user


class LoginSerializer(serializers.Serializer):
    """Сериалайзер для авторизации пользователя."""

    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True)

    user: Optional[User] = None

    def validate(self, attrs):
        """Пробуем авторизовать пользователя."""
        email = attrs.get('email')
        password = attrs.get('password')
        check_django_user(email=email)

        self.user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )

        return super().validate(attrs)  # type: ignore
