import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'server.settings')

app = Celery('server')
app.config_from_object(settings.CELERY)  # type: ignore
app.autodiscover_tasks()

app.conf.beat_schedule = {}


app.conf.beat_schedule = {
    # Отправлять на почту информацию о новых объектах.
    'send-data-to-the-user-by-subscription-on-email-constantly': {
        'task': 'send_data_to_the_user_by_subscription_on_email',
        'schedule': crontab(
            minute=settings.SEND_DATA_TO_THE_USER_BY_SUBSCRIPTION_MINUTE,
            hour='*',
        ),
    },
    # Отправлять в телеграм информацию о новых объектах.
    'send-data-to-the-user-by-subscription-on-telegram-constantly': {
        'task': 'send_data_to_the_user_by_subscription_on_telegram',
        'schedule': crontab(
            minute=settings.SEND_DATA_TO_THE_USER_BY_SUBSCRIPTION_MINUTE,
            hour='*',
        ),
    },
}
