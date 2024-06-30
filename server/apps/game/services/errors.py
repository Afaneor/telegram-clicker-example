from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException


class AlreadyBoughtError(APIException):
    """Ошибка, если предмет уже куплен."""
    status_code = 400
    default_detail = _('Пользователь уже купил этот предмет.')
    default_code = 'already_bought'


class NoItemForUserError(APIException):
    """Ошибка, если предмета нет у пользователя."""
    status_code = 400
    default_detail = _('Пользователь не имеет этот предмет.')
    default_code = 'no_item_for_user'


class NotEnoughMoneyError(APIException):
    """Ошибка, если не хватает денег."""
    status_code = 400
    default_detail = _('Недостаточно денег.')
    default_code = 'not_enough_money'
