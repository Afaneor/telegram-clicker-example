import logging

import sentry_sdk
from celery.exceptions import NotConfigured
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from server.settings.components import config

# Sentry
# ------------------------------------------------------------------------------
SENTRY_DSN = config('SENTRY_DSN', cast=str, default='')
SENTRY_LOG_LEVEL = config(
    'DJANGO_SENTRY_LOG_LEVEL',
    cast=int,
    default=logging.INFO,
)


if SENTRY_DSN:  # noqa: C901
    extra_params = {
        'environment': config(
            'SENTRY_ENVIRONMENT',
            cast=str,
            default='unknown',
        ),
    }

    if deployment := config('SENTRY_DEPLOYMENT', cast=str, default=''):
        sentry_sdk.set_tag('deployment', deployment)
    else:
        raise NotConfigured(
            'Если указан SENTRY_DSN, необходимо указать ' +
            'название развёртывания(SENTRY_DEPLOYMENT)',
        )

    # Настройка мониторинга производительности через Sentry
    traces_sample_rate = config(
        'SENTRY_TRACES_SAMPLE_RATE',
        cast=float,
        default=0,
    )
    if traces_sample_rate:
        extra_params['traces_sample_rate'] = traces_sample_rate

    sentry_logging = LoggingIntegration(
        level=SENTRY_LOG_LEVEL,  # Capture info and above as breadcrumbs
        event_level=logging.ERROR,  # Send errors as events
    )

    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            sentry_logging,
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        **extra_params,
    )
