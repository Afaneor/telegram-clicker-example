"""
Django settings for server project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their config, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""
import sys
from typing import Dict, List, Tuple, Union

from django.utils.translation import gettext_lazy as _

from server.settings.components import BASE_DIR, config

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

SECRET_KEY = config('DJANGO_SECRET_KEY')

# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1

# Application definition:
INSTALLED_APPS: Tuple[str, ...] = (
    # django-admin:
    'admin_tools_stats',  # this must be BEFORE 'admin_tools' and 'django.contrib.admin'
    'django_nvd3',
    'admin_tools',
    'admin_tools.theming',
    'admin_tools.menu',
    'admin_tools.dashboard',
    'django.contrib.admin',
    'django.contrib.admindocs',


    'corsheaders',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.staticfiles',


    # django rest framework
    'rest_framework',
    'django_filters',
    'allauth',
    'allauth.account',
    'rules',
    'django_celery_beat',

    # Your apps go here:
    'server.apps.user',
    'server.apps.game',

    # documentation
    'drf_yasg',

    # Health checks:
    # You may want to enable other checks as well,
    # see: https://github.com/KristianOellegaard/django-health-check
    'health_check',
    'health_check.db',
    'health_check.cache',
    'health_check.storage',
)

MIDDLEWARE: Tuple[str, ...] = (
    'server.apps.services.middleware.DisableCSRFMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    # Content Security Policy:
    # 'csp.middleware.CSPMiddleware',
    # Django:
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    # Django HTTP Referrer Policy:
    'django_http_referrer_policy.middleware.ReferrerPolicyMiddleware',
)

ROOT_URLCONF = 'server.urls'

WSGI_APPLICATION = 'server.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('POSTGRES_DB', default='clicker'),
        'USER': config('POSTGRES_USER', default='postgres'),
        'PASSWORD': config('POSTGRES_PASSWORD', default=''),
        'HOST': config('DJANGO_DATABASE_HOST', default='localhost'),
        'PORT': config('DJANGO_DATABASE_PORT', cast=int, default=5432),
        'CONN_MAX_AGE': config('CONN_MAX_AGE', cast=int, default=60),
        'OPTIONS': {
            'connect_timeout': 10,
            'options': '-c statement_timeout=30000',
        },
    },
}


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
)

LOCALE_PATHS = (
    'locale/',
)

USE_TZ = True
TIME_ZONE = 'UTC'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.joinpath('static')

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Templates
# https://docs.djangoproject.com/en/2.2/ref/templates/api

TEMPLATES = [{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [
        # Contains plain text templates, like `robots.txt`:
        BASE_DIR.joinpath('server', 'templates'),
    ],
    # 'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            # Default template context processors:
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.debug',
            'django.template.context_processors.i18n',
            'django.template.context_processors.media',
            'django.template.context_processors.static',
            'django.template.context_processors.tz',
            'django.contrib.messages.context_processors.messages',
            'django.template.context_processors.request',
        ],
        'loaders': [
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
            'admin_tools.template_loaders.Loader',
        ],
    },
}]

# Media files
# Media root dir is commonly changed in production
# (see development.py and production.py).
# https://docs.djangoproject.com/en/2.2/topics/files/

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR.joinpath('media')

# Django authentication system
# https://docs.djangoproject.com/en/2.2/topics/auth/

AUTHENTICATION_BACKENDS = (
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'server.apps.services.authentication_backend.TelegramAuthBackend',
)

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

# Security
CSRF_COOKIE_HTTPONLY = False

REFERRER_POLICY = 'same-origin'
# https://github.com/adamchainz/django-permissions-policy#setting
PERMISSIONS_POLICY: Dict[str, Union[str, List[str]]] = {}  # noqa: WPS234

# Timeouts
# https://docs.djangoproject.com/en/2.2/ref/settings/#std:setting-EMAIL_TIMEOUT

EMAIL_TIMEOUT = 5

AUTH_USER_MODEL = 'user.User'

# Детекция запущено ли сейчас тестирование
TESTING = 'test' in sys.argv
TESTING = TESTING or 'test_coverage' in sys.argv or 'pytest' in sys.modules

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'server.apps.services.authentication_backend.TelegramAuthBackend',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.OrderingFilter',
        'rest_framework.filters.SearchFilter',
    ),
}
