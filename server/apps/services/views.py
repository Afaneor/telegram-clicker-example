from typing import Optional, Type

from rest_framework import mixins
from rest_framework.serializers import Serializer
from rest_framework.viewsets import (
    GenericViewSet,
    ModelViewSet,
    ReadOnlyModelViewSet,
)
from rest_framework_extensions.mixins import NestedViewSetMixin
from rules.contrib.rest_framework import AutoPermissionViewSetMixin


class ViewSetSerializerMixin:  # noqa: WPS306, WPS338
    """Миксин позволяет не переопределять get_serializer_class().

    В ViesSet можно сразу указать нужный сериалайзер для action.
    Serializer_class - для GET (получение объекта).
    Create_serializer_class - для POST.
    Update_serializer_class - для PUT, PATCH.
    list_serializer_class - для GET (получение списка).
    """

    create_serializer_class: Optional[Serializer] = None
    update_serializer_class: Optional[Serializer] = None
    list_serializer_class: Optional[Serializer] = None

    def _get_serializer_class(
        self,
        *args,
        **kwargs,
    ) -> Optional[Type[Serializer]]:
        """Каждый action обладает собственным сериалазйером.

        Можно указывать во ViewSet.
        """
        if self.action == 'create':  # type: ignore
            return self.create_serializer_class
        if self.action in {'update', 'partial_update'}:  # type: ignore
            return self.update_serializer_class or self.create_serializer_class
        if self.action == 'list':  # type: ignore
            return self.list_serializer_class
        return None

    def get_serializer_class(self) -> Type[Serializer]:
        """Возвращаем класс сериалайзера с учетом action."""
        serializer_class = self._get_serializer_class()
        if serializer_class:
            return serializer_class
        return super().get_serializer_class()  # type: ignore


class RetrieveListViewSet(  # noqa: WPS215
    AutoPermissionViewSetMixin,
    NestedViewSetMixin,
    ViewSetSerializerMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    """Стандартный ReadOnlyViewSet."""

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }


class BaseModelViewSet(  # noqa: WPS215
    AutoPermissionViewSetMixin,
    NestedViewSetMixin,
    ViewSetSerializerMixin,
    ModelViewSet,
):
    """Стандартный ViewSet."""

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }


class RetrieveListCreateDeleteViewSet(  # noqa: WPS215
    ViewSetSerializerMixin,
    AutoPermissionViewSetMixin,
    NestedViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """ViewSet с возможностью просмотра/добавления/удаления."""

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }


class RetrieveListCreateUpdateViewSet(  # noqa: WPS215
    ViewSetSerializerMixin,
    AutoPermissionViewSetMixin,
    NestedViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    """ViewSet с возможностью просмотра/добавления/изменения."""

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }


class RetrieveListUpdateViewSet(  # noqa: WPS215
    ViewSetSerializerMixin,
    AutoPermissionViewSetMixin,
    NestedViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet,
):
    """ViewSet с возможностью просмотра/изменения."""

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }


class RetrieveListDeleteViewSet(  # noqa: WPS215
    ViewSetSerializerMixin,
    AutoPermissionViewSetMixin,
    NestedViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """ViewSet с возможностью просмотра/удаления."""

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }


class RetrieveListCreateUpdateDeleteViewSet(  # noqa: WPS215
    ViewSetSerializerMixin,
    AutoPermissionViewSetMixin,
    NestedViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """ViewSet с возможностью просмотра/добавления/изменения/удаления."""

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }


class RetrieveListCreateViewSet(  # noqa: WPS215
    ViewSetSerializerMixin,
    AutoPermissionViewSetMixin,
    NestedViewSetMixin,
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    GenericViewSet,
):
    """ViewSet с возможностью просмотра/добавления."""

    permission_type_map = {
        **AutoPermissionViewSetMixin.permission_type_map,
        'list': 'list',
        'metadata': None,
    }
