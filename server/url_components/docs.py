from csp.decorators import csp_exempt
from django.urls import re_path
from django.utils.translation import gettext_lazy as _
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title=_('Backend'),
        default_version='v1',
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

# Документация по API(ReDoc и Swagger)
docs_urlpatterns = [
    re_path(
        '^swagger(?P<format>.json|.yaml)$',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    re_path(
        '^swagger/$',
        csp_exempt(schema_view.with_ui('swagger', cache_timeout=0)),
        name='schema-swagger-ui',
    ),
    re_path(
        '^redoc/$',
        csp_exempt(schema_view.with_ui('redoc', cache_timeout=0)),
        name='schema-redoc',
    ),
]
