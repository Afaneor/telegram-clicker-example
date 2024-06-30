from django.db import models
from django.utils.translation import gettext_lazy as _
from rules.contrib.models import RulesModelBase, RulesModelMixin


class AbstractBaseModel(  # type: ignore
    RulesModelMixin,
    models.Model,
    metaclass=RulesModelBase,
):
    """Базовая модель."""

    created_at = models.DateTimeField(
        verbose_name=_('Создан'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Изменен'),
        auto_now=True,
    )

    class Meta:
        abstract = True
        ordering = ['-id']
