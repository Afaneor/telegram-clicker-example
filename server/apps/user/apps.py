from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UserConfig(AppConfig):
    """Конфиг приложения с пользователями."""

    name = 'server.apps.user'
    label = 'user'
    verbose_name = _('Пользователь')

    def ready(self):
        """Подключение роутера и прав происходит при подключении app."""
        super().ready()
        import server.apps.user.api.routers
        import server.apps.user.permissions

