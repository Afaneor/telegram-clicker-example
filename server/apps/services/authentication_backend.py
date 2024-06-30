import hashlib
import hmac
import time

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from rest_framework import status
from rest_framework.exceptions import APIException
from django.utils.translation import gettext_lazy as _
from django.conf import settings

User = get_user_model()


class InvalidAuthData(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Неверные данные авторизации.')
    default_code = 'invalid_auth_data'


class TelegramAuthBackend(BaseBackend):
    def authenticate(self, request, **kwargs):
        self.validate_telegram_auth_data(kwargs, bot_token=settings.TELEGRAM_BOT_TOKEN)
        try:
            return User.objects.get(username=kwargs['username'])
        except User.DoesNotExist:
            return None

    def validate_telegram_auth_data(self, auth_data: dict, bot_token: str) -> dict:
        """Валидация данных авторизации."""
        check_hash = auth_data.pop('hash')
        data_check_arr = [f"{key}={value}" for key, value in auth_data.items()]
        data_check_arr.sort()
        data_check_string = "\n".join(data_check_arr)
        secret_key = hashlib.sha256(bot_token.encode()).digest()
        hash = hmac.new(secret_key, data_check_string.encode(), hashlib.sha256).hexdigest()

        if hash != check_hash:
            raise InvalidAuthData()

        if (time.time() - auth_data['auth_date']) > 86400:
            raise InvalidAuthData()
        return auth_data

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
