import sys

from django.conf import settings

from server.settings.components import config

# Детекция запущено ли сейчас тестирование
TESTING = 'test' in sys.argv
TESTING = TESTING or 'test_coverage' in sys.argv or 'pytest' in sys.modules

CELERY = {
    'broker_url': config(
        'CELERY_BROKER_URL',
        default='amqp://guest:guest@localhost:5672/',
        cast=str,
    ),
    'task_always_eager': settings.TESTING,  # type: ignore
    'worker_hijack_root_logger': False,
    'timezone': settings.TIME_ZONE,
}
