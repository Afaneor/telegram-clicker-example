from typing import TYPE_CHECKING

from django.db import transaction

from server.apps.game.models.income_item import IncomeItem, UserIncomeItem
from server.apps.game.services.api.user import UserAPI
from server.apps.game.services.errors import (
    AlreadyBoughtError,
    NoItemForUserError,
    NotEnoughMoneyError,
)

if TYPE_CHECKING:
    from server.apps.user.models import User


class IncomeItemService(object):
    """Бизнес логика для IncomeItem."""
    def buy(self, income_item: IncomeItem, user: 'User'):
        """Метод для покупки предмета."""
        if self._get_user_item(income_item, user):
            raise AlreadyBoughtError()

        user_api = UserAPI()

        if user_api.get_user_available_balance(user) < income_item.base_price:
            raise NotEnoughMoneyError()

        with transaction.atomic():
            user_api.claim(user)
            user.balance -= income_item.base_price
            user.save()

            UserIncomeItem.objects.create(
                user=user,
                item=income_item,
                level=1,
            )

    def upgrade(self, income_item: IncomeItem, user: 'User'):
        """Метод для улучшения предмета."""
        user_item = self._get_user_item(income_item, user)
        if not user_item:
            raise NoItemForUserError()

        item_price = income_item.base_price * (income_item.price_multiplier ** user_item.level)
        user_api = UserAPI()
        if user_api.get_user_available_balance(user) < item_price:
            raise NotEnoughMoneyError()

        with transaction.atomic():
            user_api.claim(user)
            user.balance -= item_price
            user.save()

            user_item.level += 1
            user_item.save()

    @staticmethod
    def _get_user_item(income_item: IncomeItem, user: 'User') -> UserIncomeItem | None:
        """Метод для проверки наличия предмета у пользователя."""
        try:
            return UserIncomeItem.objects.get(user=user, item=income_item)
        except UserIncomeItem.DoesNotExist:
            return None
