from django.utils.translation import gettext as _
from rest_framework.exceptions import NotFound, ValidationError

from server.apps.user.models import User


def check_django_user(email: str) -> User:
    """Проверка, что пользователь с заданным email существует."""
    try:
        User.objects.get(email=email)
    except User.DoesNotExist:
        raise NotFound(_('Пользователь с указанными данными не найден'))


def get_django_user(email: str) -> User:
    """Получить пользователя с заданным email существует."""
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise NotFound(_('Пользователь с указанными данными не найден'))
    return user


def check_user_active(email: str) -> User:
    """Поиск пользователя с заданным email."""
    user = get_django_user(email=email)

    if user.is_active:
        raise ValidationError(
            {'email': [_('Пользователь с указанным email уже активен')]},
        )
    return user


