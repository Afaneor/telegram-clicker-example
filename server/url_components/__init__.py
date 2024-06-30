from server.url_components.admin import admin_urlpatterns
from server.url_components.docs import docs_urlpatterns
from server.url_components.errors import handler500
from server.url_components.jwt import jwt_urlpatterns
from server.url_components.seo import seo_urlpatterns

__all__ = [
    'seo_urlpatterns',
    'admin_urlpatterns',
    'docs_urlpatterns',
    'jwt_urlpatterns',
    'handler500',
]
