from datetime import datetime

from django.db.models import F, Sum
from django.db.models.functions import Power

from server.apps.user.models import User


class UserService:
    """Сервис для работы с пользователями."""

    @staticmethod
    def get_user_income_per_second(user: User) -> int:
        """Получаем доход пользователя в секунду."""
        income = user.user_income_items.select_related('item').annotate(
            income=F('item__base_income') * Power(F('item__income_multiplier'), F('level'))
        ).aggregate(
            total_income=Sum('income')
        )['total_income'] or 0
        return income

    @staticmethod
    def get_user_available_balance(user: User) -> int:
        """Получаем доступный баланс пользователя."""
        ts = int(datetime.utcnow().timestamp())
        income = UserService.get_user_income_per_second(user)
        seconds_passed = ts - user.last_claimed
        return user.balance + int(seconds_passed * income)

    @staticmethod
    def claim(user: User) -> None:
        """Обновляем баланс пользователя."""
        user.balance = UserService.get_user_available_balance(user)
        user.last_claimed = int(datetime.utcnow().timestamp())
        user.save()

    @staticmethod
    def update_balance_with_clicks(user: User, clicks: int) -> None:
        """Обновляем баланс пользователя."""
        user.balance += clicks
        user.last_balance_update = int(datetime.utcnow().timestamp())
        user.save()
