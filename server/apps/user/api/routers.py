from rest_framework.routers import APIRootView

from server.apps.services.custom_router.api_router import ApiRouter
from server.apps.user.api.views import UserViewSet


class UserAPIRootView(APIRootView):
    """Корневой view для апи."""

    __doc__ = 'Приложение пользователей'
    name = 'user'


router = ApiRouter()
router.APIRootView = UserAPIRootView

router.register('users', UserViewSet, 'users')
