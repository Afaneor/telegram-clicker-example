from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class IncomeItem(AbstractBaseModel):
    """Модель предмета для дохода."""

    name = models.CharField(
        verbose_name=_('название'),
        max_length=255,
    )
    icon = models.ImageField(
        verbose_name=_('иконка'),
        upload_to='farm_items',
        null=True,
    )
    base_price = models.IntegerField(
        verbose_name=_('базовая цена'),
    )
    base_income = models.IntegerField(
        verbose_name=_('базовый доход в секунду'),
    )
    income_multiplier = models.FloatField(
        verbose_name=_('множитель дохода'),
        default=1.0,
    )
    price_multiplier = models.FloatField(
        verbose_name=_('множитель цены'),
        default=1.0,
    )
    visible = models.BooleanField(
        verbose_name=_('видимость'),
        default=False,
    )

    user_items = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        verbose_name=_('пользовательские предметы'),
        through='game.UserIncomeItem',
    )

    class Meta:
        verbose_name = _('Предмет для дохода')
        verbose_name_plural = _('Предметы для дохода')

    def __str__(self):
        return self.name


class UserIncomeItem(AbstractBaseModel):
    """Модель предмета для дохода пользователя."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('пользователь'),
        related_name='user_income_items',
        on_delete=models.CASCADE,
        db_index=True,
    )
    item = models.ForeignKey(
        IncomeItem,
        verbose_name=_('предмет для дохода'),
        related_name='user_income_items',
        on_delete=models.CASCADE,
        db_index=True,
    )
    level = models.IntegerField(
        verbose_name=_('количество'),
        default=1,
    )

    class Meta:
        verbose_name = _('Пользовательский предмет для дохода')
        verbose_name_plural = _('Пользовательские предметы для дохода')
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'item'],
                name='unique_user_item',
            ),
        ]

    def __str__(self):
        return f'{self.user} - {self.item}'
