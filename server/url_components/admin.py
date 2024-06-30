from django.contrib import admin
from django.contrib.admindocs import urls as admindocs_urls
from django.urls import include, path

admin_urlpatterns = [
    path('admin/doc/', include(admindocs_urls)),  # noqa: DJ05
    path('admin/', admin.site.urls),
]
