from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet

from server.apps.game.api.serializers.promo import PromoSerializer
from server.apps.game.models import Promo


class PromoViewSet(
    ListModelMixin,
    GenericViewSet
):
    """
    ViewSet для промо.
    """

    queryset = Promo.objects.filter(visible=True)
    serializer_class = PromoSerializer

    @action(detail=True, methods=['post'])
    def claim(self, request, *args, **kwargs):
        promo = self.get_object()

