from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModelBase, RulesModelMixin


class User(  # type: ignore
    RulesModelMixin,
    AbstractUser,
    metaclass=RulesModelBase,
):
    """Кастомный класс пользователя."""

    USERNAME_FIELD = 'username'

    avatar = models.URLField(
        verbose_name=_('Аватар'),
        blank=True,
    )
    referrer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Кто пригласил'),
        on_delete=models.SET_NULL,
        null=True,
        related_name='referrals',
    )
    last_claimed = models.IntegerField(
        verbose_name=_('Последний раз забирали монеты в игре, unix timestamp'),
    )
    last_balance_update = models.IntegerField(
        verbose_name=_('Последнее обновление баланса (клики), unix timestamp'),
    )
    balance = models.BigIntegerField(
        verbose_name=_('Баланс'),
        default=0,
    )

    class Meta:
        verbose_name = _('Пользователь')
        verbose_name_plural = _('Пользователи')

    def __str__(self):
        return self.username

    def save(
        self,
        *args,
        **kwargs,
    ):
        # значит это новый пользователь
        if not self.pk:
            ts = int(datetime.utcnow().timestamp())
            self.last_balance_update = int(ts)
            self.last_claimed = int(ts)
        super().save(*args, **kwargs)
