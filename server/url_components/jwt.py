from django.urls import path
from rest_framework_simplejwt.views import (
    token_obtain_pair,
    token_refresh,
    token_verify,
)

jwt_urlpatterns = [
    path('api/auth/obtain-token/', token_obtain_pair),
    path('api/auth/refresh-token/', token_refresh),
    path('api/auth/verify-token/', token_verify),
]
