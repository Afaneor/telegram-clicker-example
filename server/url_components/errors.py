import sentry_sdk
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from django.views.defaults import server_error
from rest_framework import status


def handler500(request, exception=None):
    """Обработчик 500х ошибок.

    При запросе типа JSON будет возвращаться ответ в виде JSON с id ошибки в
    Sentry
    """
    if request.content_type == 'application/json':
        return JsonResponse(
            {
                'error': _(
                    'Произошла ошибка на сервере. Команда разработки ' +
                    'уже работает над устранением проблемы.',
                ),
                'sentryEventId': sentry_sdk.last_event_id(),
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            charset='utf-8',
        )
    return server_error(request)
