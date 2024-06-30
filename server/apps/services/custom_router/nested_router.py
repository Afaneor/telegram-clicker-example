from __future__ import annotations

from collections import defaultdict
from typing import Iterable, Optional, Union

from rest_framework.routers import BaseRouter, SimpleRouter
from rest_framework.viewsets import ViewSet
from rest_framework_extensions.utils import compose_parent_pk_kwarg_name


class NestedRegistryItem(object):
    """Зарегитрированный в SimpleRouter-e элемент."""

    def __init__(  # noqa: WPS211
        self,
        router,
        parent_prefix,
        parent_item=None,
        parent_viewset=None,
        parent_basename=None,
    ):
        """Не знаю, что тут комментировать."""
        self.router = router
        self.parent_prefix = parent_prefix
        self.parent_item = parent_item
        self.parent_viewset = parent_viewset
        self.parent_basename = parent_basename

    def register(  # noqa: WPS211
        self,
        prefix: str,
        viewset_or_router: Union[BaseRouter, ViewSet, NestedRegistryItem],
        basename: str,
        parents_query_lookups: Iterable[str],
        link_name: Optional[str] = None,
    ) -> NestedRegistryItem:
        """
        Регистрация нового вложенного маршрута.

        :param prefix:
        :type prefix: str
        :param viewset_or_router: ViewSet или другой роутер
        :type viewset_or_router: ViewSet, BaseRouter, NestedRegistryItem
        :param basename: Название namespace, с которым будет
            зарегистрирован новый маршрут

        :type basename: str
        :param parents_query_lookups:
            Названия полей родительских сущностей, нужно указывать слева
            направо, как они идут в ссылке

        :type parents_query_lookups: Iterable[str]
        :param link_name: Название для ссылки, которое будет
            отображаться в BrowsableAPIRenderer

        :type link_name: Optional[str]
        :return: Возвращается новый маршрутизатор,
            в который можно регистрировать другие дочерние маршруты

        :rtype: NestedRegistryItem

        """
        self.router._register(
            prefix=self.prefix(
                current_prefix=prefix,
                parents_query_lookups=tuple(parents_query_lookups),
            ),
            viewset=viewset_or_router,
            basename=basename,
        )
        if not hasattr(self.parent_viewset, '_nested_routers'):  # noqa: WPS421
            self.parent_viewset._nested_routers = defaultdict(list)
        self.parent_viewset._nested_routers[self.parent_basename].append({
            'basename': basename,
            'viewset': viewset_or_router,
            'lookups': parents_query_lookups,
            'link_name': link_name,
        })
        return NestedRegistryItem(
            router=self.router,
            parent_prefix=prefix,
            parent_item=self,
            parent_viewset=viewset_or_router,
            parent_basename=basename,
        )

    def prefix(self, current_prefix, parents_query_lookups) -> str:
        """Url текущего уровня."""
        return '{0}/{1}'.format(
            self.parent_prefix(parents_query_lookups),
            current_prefix,
        )

    def parent_prefix(self, parents_query_lookups):
        """Вычисление Url родительского элемента."""
        prefix = '/'
        current_item = self
        level = len(parents_query_lookups) - 1
        while current_item:
            parent_lookup_value_regex = getattr(
                current_item.parent_viewset,
                'lookup_value_regex',
                '[^/.]+',
            )
            prefix = (
                '{parent_prefix}/(?P<{parent_pk_kwarg_name}>' +
                '{parent_lookup_value_regex})/{prefix}'
            ).format(
                parent_prefix=current_item.parent_prefix,
                parent_pk_kwarg_name=compose_parent_pk_kwarg_name(
                    parents_query_lookups[level],
                ),
                parent_lookup_value_regex=parent_lookup_value_regex,
                prefix=prefix,
            )
            level -= 1
            current_item = current_item.parent_item
        return prefix.strip('/')


class NestedRouterMixin(object):
    """Миксин, добавляющий регистрацию в роутере с генерацией item."""

    def register(self, *args, **kwargs):
        """Регистрация router-a или viewset-a."""
        super().register(*args, **kwargs)
        return NestedRegistryItem(
            router=self,
            parent_prefix=self.registry[-1][0],
            parent_viewset=self.registry[-1][1],
            parent_basename=kwargs.get('basename', None),
        )


class NestedSimpleRouter(NestedRouterMixin, SimpleRouter):
    """Роутер на экспорт."""
