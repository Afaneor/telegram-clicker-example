from django.db.models import Prefetch, QuerySet
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from server.apps.game.api.serializers.income_item import IncomeItemSerializer
from server.apps.game.models.income_item import IncomeItem, UserIncomeItem
from server.apps.game.services.income_item import IncomeItemService


class IncomeItemViewSet(
    ListModelMixin,
    GenericViewSet
):
    """
    ViewSet для предметов дохода.
    """

    queryset = IncomeItem.objects.filter(visible=True)
    serializer_class = IncomeItemSerializer

    def list(self, request, *args, **kwargs):
        queryset: QuerySet[IncomeItem] = self.filter_queryset(self.get_queryset())
        queryset.prefetch_related(
            Prefetch(
                'user_income_items',
                queryset=UserIncomeItem.objects.filter(user=request.user),
            )
        )

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def buy(self, request, *args, **kwargs):
        user = request.user
        income_item = self.get_object()
        IncomeItemService().buy(income_item, user)
        return Response(status=200)

    @action(detail=True, methods=['post'])
    def upgrade(self, request, *args, **kwargs):
        user = request.user
        income_item = self.get_object()
        IncomeItemService().upgrade(income_item, user)
        return Response(status=200)
