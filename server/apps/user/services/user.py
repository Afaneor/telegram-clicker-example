from datetime import datetime

from django.db.models import F, Sum
from django.db.models.functions import Power
from server.apps.user.models import User


class UserService:
    """Сервис для работы с пользователями."""
    @staticmethod
    def get_user_available_balance(user: User) -> int:
        """Получаем доступный баланс пользователя."""
        ts = int(datetime.utcnow().timestamp())
        seconds_passed = ts - user.last_balance_update
        income = user.user_income_items.select_related('item').annotate(
            income=F('item__base_income') * Power(F('item__income_multiplier'), F('level')) * seconds_passed
        ).aggregate(
            total_income=Sum('income')
        )['total_income'] or 0
        return user.balance + int(income)

    @staticmethod
    def claim(user: User) -> None:
        """Обновляем баланс пользователя."""
        user.balance = UserService.get_user_available_balance(user)
        user.last_claimed = int(datetime.utcnow().timestamp())
        user.save()
