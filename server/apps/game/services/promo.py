from django.db import transaction
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import APIException

from server.apps.game.models import Promo
from server.apps.user.models import User


class AlreadyClaimedError(APIException):
    status_code = 400
    default_detail = _('Промо уже активировано.')
    default_code = 'promo_already_claimed'


class PromoService(object):

    @staticmethod
    def claim(promo: Promo, user: User) -> int:
        """Метод для активации промо."""
        if promo.users_claimed.filter(id=user.id).exists():
            raise AlreadyClaimedError()

        with transaction.atomic():
            user.balance += promo.reward
            user.save()
            # TODO можно сделать классы для валидации, что человек что-то сделал и т.д.
            promo.users_claimed.add(user)
        return user.balance
