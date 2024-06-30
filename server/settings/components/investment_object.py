from server.settings.components import config

MAX_STRING_LENGTH = 255

# Переменные для работы DaData.
DADATA_API_TOKEN = config('DADATA_API_TOKEN', default='token', cast=str)
DADATA_API_URL = config(
    'DADATA_API_URL',
    default='https://suggestions.dadata.ru/suggestions/api/4_1/rs',
    cast=str,
)
DADATA_TIMEOUT_SEC = 5


USERS_PASSWORD_RESET_REVERSE_URL = 'api:user:users-reset-password-process'

USERS_CONFIRM_EMAIL_REVERSE_URL = 'api:user:users-confirm-email-process'

OPENAI_API_KEY = config(
    'OPENAI_API_KEY',
    default='',
    cast=str
)

PSPDFKIT_API_SECRET_KEY = config(
    'PSPDFKIT_API_SECRET_KEY',
    default='',
    cast=str
)

DJANGO_SUPERUSER_EMAIL = config(
    'DJANGO_SUPERUSER_EMAIL',
    default='admin@dolma.ru',
    cast=str
)

DJANGO_SUPERUSER_PASSWORD = config(
    'DJANGO_SUPERUSER_PASSWORD',
    default='1234',
    cast=str
)

SEND_DATA_TO_THE_USER_BY_SUBSCRIPTION_MINUTE = config(
    'SEND_DATA_TO_THE_USER_BY_SUBSCRIPTION_MINUTE',
    default=5,
    cast=int
)

DOCUMENT_CONVERTER_URL = config(
    'DOCUMENT_CONVERTER_URL',
    default='http://gotenberg:3000',
    cast=str
)
