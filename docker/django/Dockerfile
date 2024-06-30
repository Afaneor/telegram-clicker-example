# This Dockerfile uses multi-stage build to customize DEV and PROD images:
# https://docs.docker.com/develop/develop-images/multistage-build/

FROM hub.letsnova.com/p/python:3.11-slim-bookworm AS base_build

LABEL maintainer="dolma@tech.ru"
LABEL vendor="dolma"

ENV \
  # build:
  BUILD_ONLY_PACKAGES='wget gnupg lsb-release' \
  # python:
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PYTHONDONTWRITEBYTECODE=1 \
  # pip:
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  PIP_INDEX_URL=https://pypi.python.org/simple/ \
  # dockerize:
  USE_DOCKER=1 \
  DOCKERIZE_VERSION=v0.6.1 \
  # tini:
  TINI_VERSION=v0.19.0 \
  # poetry:
  POETRY_VERSION=1.4.2\
  POETRY_NO_INTERACTION=1 \
  POETRY_VIRTUALENVS_CREATE=false \
  POETRY_CACHE_DIR='/var/cache/pypoetry' \
  # PostgreSQL Client major version
  PG_MAJOR_VERSION=13


# System deps:
RUN apt-get update && apt-get upgrade -y \
  && apt-get install --no-install-recommends -y \
    bash \
    curl \
    gettext \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    # Web static server
    nginx \
    # Defining build-time-only dependencies:
    $BUILD_ONLY_PACKAGES \
  # Install requirements for django-dbbackup
  && wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | apt-key add - \
  && echo "deb http://apt.postgresql.org/pub/repos/apt/ `lsb_release -cs`-pgdg main" | tee /etc/apt/sources.list.d/pgdg.list \
  && apt update \
  && apt install  --no-install-recommends -y postgresql-client-${PG_MAJOR_VERSION} \
  # Removing build-time-only dependencies:
  && apt-get remove -y $BUILD_ONLY_PACKAGES \
  # Cleaning cache:
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && apt-get clean -y && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# This is a special case. We need to run this script as an entry point:
COPY ./docker/django/entrypoint.sh /docker-entrypoint.sh

# Setting up proper permissions:
RUN chmod +x '/docker-entrypoint.sh' \
  && groupadd -r web && useradd -d /app -r -g web web \
  && chown web:web -R /app \
  && mkdir -p /var/www/django/static /var/www/django/media \
  && chown web:web /var/www/django/static /var/www/django/media

# Копируем алиасы
COPY --chown=web:web --chmod=0600 ./docker/django/.bashrc .

# Copy only requirements, to cache them in docker layer
COPY --chown=web:web ./poetry.lock ./pyproject.toml /app/

# Project initialization:
RUN poetry install --no-dev \
  && rm -rf "$POETRY_CACHE_DIR" \
  # Устанавливаем poetry заново, так как блядский poetry при установке удаляет
  # свои же зависимости
  && pip install "poetry==$POETRY_VERSION"


FROM base_build AS development_build

RUN poetry install \
  && rm -rf "$POETRY_CACHE_DIR" \
  # Устанавливаем poetry заново, так как блядский poetry при установке удаляет
  # свои же зависимости
  && pip install "poetry==$POETRY_VERSION"

# Running as non-root user:
USER web

# Pass build info environments
ARG DJANGO_ENV
ARG NOVA_RELEASE
ARG NOVA_BUILD_ID
ARG NOVA_PIPELINE_URL
ENV DJANGO_ENV=${DJANGO_ENV} \
 NOVA_RELEASE="${NOVA_RELEASE:-No CI Build}" \
 NOVA_BUILD_ID="${NOVA_BUILD_ID:-No CI Build}" \
 NOVA_PIPELINE_URL="${NOVA_PIPELINE_URL:-No CI Build}" \
 NOVA_DOCKER_IMAGE_TYPE="CI Image"

# We customize how our app is loaded with the custom entrypoint:
ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]


# The following stage is only for Prod:
# https://wemake-django-template.readthedocs.io/en/latest/pages/template/production.html
FROM base_build AS production_build

COPY ./docker/nginx /etc/nginx

# Создаём файл /var/log/nginx/error.log, чтобы nginx не ругался на права
USER root
RUN touch /var/log/nginx/error.log && chown web:web /var/log/nginx/error.log

# Копируем скрипты для старта сервера
COPY --chown=web:web ./docker/django/scripts/* /usr/local/bin/
RUN for i in /usr/local/bin/start-web-server /usr/local/bin/provision; do \
 sed -i 's/\r$//g' $i; chmod +x $i; done

USER web

HEALTHCHECK --interval=60s --timeout=3s --start-period=30s \
  CMD curl -f http://localhost:8000/health/ || exit 1

COPY --chown=web:web . /app

# Pass build info environments
ARG DJANGO_ENV
ARG NOVA_RELEASE
ARG NOVA_BUILD_ID
ARG NOVA_PIPELINE_URL
ENV DJANGO_ENV=${DJANGO_ENV} \
 NOVA_RELEASE="${NOVA_RELEASE:-No CI Build}" \
 NOVA_BUILD_ID="${NOVA_BUILD_ID:-No CI Build}" \
 NOVA_PIPELINE_URL="${NOVA_PIPELINE_URL:-No CI Build}" \
 NOVA_DOCKER_IMAGE_TYPE="Production"

ENTRYPOINT ["tini", "--", "/docker-entrypoint.sh"]
