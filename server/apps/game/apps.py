from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class GameConfig(AppConfig):
    name = 'server.apps.game'

    label = 'game'
    verbose_name = _('Clicker')
