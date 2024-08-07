from django.db.models import Exists, OuterRef
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from server.apps.game.api.serializers.promo import PromoSerializer
from server.apps.game.models import Promo
from server.apps.game.services.promo import PromoService


class PromoViewSet(
    ListModelMixin,
    GenericViewSet
):
    """
    ViewSet для промо.
    """

    queryset = Promo.objects.filter(visible=True)
    serializer_class = PromoSerializer

    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.filter_queryset(self.get_queryset())
        queryset = queryset.annotate(claimed=Exists(user.promos_claimed.filter(pk=OuterRef('pk'))))
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def claim(self, request, *args, **kwargs):
        promo = self.get_object()
        PromoService().claim(promo, request.user)
        return Response(status=200)
