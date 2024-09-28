import hashlib
import hmac
import json
import time
from typing import Optional
from urllib.parse import unquote

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException

User = get_user_model()


class InvalidAuthData(APIException):
    status_code = status.HTTP_401_UNAUTHORIZED
    default_detail = _('Неверные данные авторизации.')
    default_code = 'invalid_auth_data'


class TelegramAuthBackend(BaseBackend):
    def authenticate(self, request, **kwargs) -> Optional[User]:
        """
        Основной метод аутентификации через Telegram.
        Извлекает и валидирует данные из initData.
        """
        init_data = request.query_params.get("initData")
        if not init_data:
            return None

        try:
            # Валидация данных авторизации
            auth_data = self.validate_telegram_auth_data(
                init_data,
                bot_token=settings.TELEGRAM_BOT_TOKEN,
            )

            # Извлечение или создание пользователя
            user = json.loads(auth_data.get('user', '{}'))
            username = user.get('id')
            if not username:
                return None

            user, _ = User.objects.get_or_create(username=username)
            return user, None

        except InvalidAuthData as e:
            return None

    def validate_telegram_auth_data(
        self,
        init_data: str,
        bot_token: str,
    ) -> dict[str, str]:
        """
        Валидация данных из initData, проверка подписи и срока действия данных.
        Возвращает словарь с проверенными данными авторизации.
        """
        auth_data, hash_str = self.parse_init_data(init_data)

        # Проверка целостности данных
        self.verify_data_hash(auth_data, hash_str, bot_token)

        # Проверка срока действия данных
        self.check_auth_date(auth_data.get("auth_date"))

        return auth_data

    def parse_init_data(self, init_data: str) -> tuple[dict[str, str], str]:
        """
        Разбирает строку initData на ключ-значение, извлекает хэш.
        Возвращает кортеж: (данные авторизации без хэша, хэш).
        """
        data_list = [
            chunk.split("=", 1) for chunk in unquote(init_data).split("&")
        ]
        auth_data = {key: value for key, value in data_list if key != "hash"}
        hash_str = next((value for key, value in data_list if key == "hash"),
                        None)

        if not hash_str:
            raise InvalidAuthData("Отсутствует параметр hash в initData.")

        return auth_data, hash_str

    def verify_data_hash(self, auth_data: dict[str, str], hash_str: str,
                         bot_token: str) -> None:
        """
        Проверяет корректность хэша данных с использованием HMAC-SHA256.
        """
        # Сортируем данные и формируем строку key=value с разделителем \n
        data_check_string = "\n".join(
            f"{key}={value}" for key, value in sorted(auth_data.items()))

        # Генерируем секретный ключ HMAC-SHA256 от токена и строки "WebAppData"
        secret_key = hmac.new("WebAppData".encode(), bot_token.encode(),
                              hashlib.sha256).digest()

        # Вычисляем хэш данных
        calculated_hash = hmac.new(secret_key, data_check_string.encode(),
                                   hashlib.sha256).hexdigest()

        # Сравниваем полученный хэш с переданным
        if calculated_hash != hash_str:
            raise InvalidAuthData(
                "Хэш не совпадает, данные могут быть скомпрометированы.")

    def check_auth_date(self, auth_date_str: Optional[str]) -> None:
        """
        Проверяет срок действия данных авторизации (не старше 24 часов).
        """
        if not auth_date_str:
            raise InvalidAuthData("Отсутствует поле 'auth_date'.")

        try:
            auth_date = int(auth_date_str)
        except ValueError:
            raise InvalidAuthData(
                f"Некорректный формат 'auth_date': {auth_date_str}")

        current_time = time.time()
        if (current_time - auth_date) > 86400:
            raise InvalidAuthData("Срок авторизации истек.")

    def get_user(self, user_id: int) -> Optional[User]:
        """
        Возвращает пользователя по ID.
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None