from rest_framework.routers import APIRootView

from server.apps.services.custom_router.api_router import ApiRouter
from server.apps.game.api.views.income_item import IncomeItemViewSet
from server.apps.game.api.views.promo import PromoViewSet


class GameAPIView(APIRootView):
    """Корневой view для апи."""

    __doc__ = 'Приложение кликера'
    name = 'game'


router = ApiRouter()
router.APIRootView = GameAPIView

router.register('income-items', IncomeItemViewSet, basename='income-items')
router.register('promos', PromoViewSet, basename='promos')
