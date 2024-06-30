from rest_framework import status
from rest_framework.exceptions import APIException


class ApiError(APIException):
    """Ошибка API."""

    status_code = status.HTTP_400_BAD_REQUEST


class SendEmailError(APIException):
    """Ошибка при отправке письма с подтверждением регистрации."""

    status_code = status.HTTP_501_NOT_IMPLEMENTED