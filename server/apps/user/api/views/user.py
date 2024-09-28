import django_filters
from django.contrib.auth import authenticate
from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.request import Request
from rest_framework.response import Response

from server.apps.services.views import RetrieveListUpdateViewSet
from server.apps.user.api.serializers import UserSerializer
from server.apps.user.api.serializers.user import UserClicksSerializer
from server.apps.user.models import User
from server.apps.user.services.user import UserService


class UserFilter(django_filters.FilterSet):
    """Фильтр для модели пользователя."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'is_active',
        )


class UserViewSet(RetrieveListUpdateViewSet):
    """
    Пользователи.
    """

    serializer_class = UserSerializer
    queryset = User.objects.all()
    filterset_class = UserFilter
    ordering_fields = '__all__'
    permission_type_map = {
        **RetrieveListUpdateViewSet.permission_type_map,
        'get_info': None,
        'clicks': 'list',
    }

    def get_queryset(self):
        """Выдача информации о пользователях."""
        queryset = super().get_queryset()
        user = self.request.user

        return queryset.filter(Q(referrer=user) | Q(id=user.id))

    @action(
        methods=['GET'],
        detail=False,
        url_path='get-info',
        serializer_class=UserSerializer,
    )
    def get_info(self, request: Request):
        """Получение информации о пользователе.

        Детальная информация о пользователе.
        """
        user = request.user

        if user.is_anonymous:
            auth_data = request.query_params
            user = authenticate(request, **auth_data)

        if user is None:
            return Response(
                status=status.HTTP_401_UNAUTHORIZED,
            )
        UserService.claim(user)
        return Response(
            data=self.serializer_class(user).data,
            status=status.HTTP_200_OK,
        )


    @action(
        methods=['POST'],
        url_path='clicks',
        detail=False,
        serializer_class=UserClicksSerializer,
    )
    def clicks(self, request: Request):
        """Обновление баланса пользователя.

        Обновление баланса пользователя.
        """
        serializer = self.get_serializer_class()(data=request.data)
        serializer.is_valid(raise_exception=True)

        UserService.update_balance_with_clicks(
            user=request.user,
            clicks=serializer.validated_data['clicks'],
        )
        UserService.claim(request.user)

        return Response(
            data=UserSerializer(request.user).data,
            status=status.HTTP_200_OK,
        )
