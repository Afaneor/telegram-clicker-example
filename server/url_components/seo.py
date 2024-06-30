from django.urls import path
from django.views.generic import TemplateView

seo_urlpatterns = [
    path(
        'robots.txt',
        TemplateView.as_view(
            template_name='txt/robots.txt', content_type='text/plain',
        ),
    ),
    path(
        'humans.txt',
        TemplateView.as_view(
            template_name='txt/humans.txt', content_type='text/plain',
        ),
    ),
]
