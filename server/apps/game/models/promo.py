from django.db import models
from django.utils.translation import gettext_lazy as _

from server.apps.services.base_model import AbstractBaseModel


class Promo(AbstractBaseModel):
    """Модель промоакций."""
    name = models.TextField(
        verbose_name=_('Название'),
        max_length=255,
    )
    reward = models.IntegerField(
        verbose_name=_('Награда'),
    )
    visible = models.BooleanField(
        verbose_name=_('Достпность для просмотра'),
        default=False,
    )

    users_claimed = models.ManyToManyField(
        'user.User',
        verbose_name=_('Пользователи, которые промо'),
        related_name='promos_claimed',
    )

    class Meta:
        verbose_name = _('Промокод')
        verbose_name_plural = _('Промокоды')

    def __str__(self):
        return f'{self.name} - {self.reward}'
