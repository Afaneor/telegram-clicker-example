from collections import OrderedDict

from django.urls import NoReverseMatch, include, re_path
from django.urls import reverse as django_reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import reverse
from rest_framework.routers import APIRootView, DefaultRouter, SimpleRouter
from rest_framework.views import APIView


class ApiRouter(DefaultRouter):
    """
    Расширение для drf.DefaultRouter.

    Теперь можно регистрировать как DRF ViewSets, так и другие роутеры
    Примеры использования:
    1. Тут регистрируется другой роутер
    2. Тут регистрируется ViewSet
    router.register('organizations', OrganizationViewSet)  # noqa: F821
    """

    def get_urls(self):  # noqa: WPS210
        """Use the registered viewsets to generate a list of URL patterns."""
        ret = []

        for prefix, viewset, basename in self.registry:
            if isinstance(viewset, (SimpleRouter, DefaultRouter)):
                ret.append(
                    re_path(
                        f'{prefix}/',
                        include((viewset.urls, basename), basename),
                    ),
                )
            elif issubclass(viewset, APIView):
                ret += self._get_urls_for_viewset(  # type: ignore
                    prefix, viewset, basename,
                )

        urls = ret

        if self.include_root_view:
            view = self.get_api_root_view(api_urls=urls)  # type: ignore
            root_url = re_path(r'^$', view, name=self.root_view_name)  # noqa: WPS360, E501
            urls.append(root_url)

        return urls

    def get_routes(self, viewset):
        """
        Augment `self.routes` with any dynamically generated routes.

        Returns a list of the Route namedtuple.
        """
        # converting to list as iterables are good for one pass,
        # known host needs to be checked again and again for
        # different functions.
        if not isinstance(viewset, (SimpleRouter, DefaultRouter)):
            return super().get_routes(viewset)

    def get_api_root_view(self, api_urls=None):
        """Return a basic root view."""
        api_root_dict = OrderedDict()
        list_name = self.routes[0].name
        for prefix, viewset, basename in self.registry:
            if isinstance(viewset, (SimpleRouter, DefaultRouter)):
                api_root_dict[prefix] = f'{basename}:{viewset.root_view_name}'
            else:
                api_root_dict[prefix] = list_name.format(basename=basename)

        return self.APIRootView.as_view(api_root_dict=api_root_dict)

    def _get_urls_for_viewset(self, prefix, viewset, basename):  # noqa: WPS210
        ret = []
        lookup = self.get_lookup_regex(viewset)
        routes = self.get_routes(viewset)  # type: ignore

        for route in routes:
            # Only actions which actually exist on the viewset will be bound
            mapping = self.get_method_map(viewset, route.mapping)
            if not mapping:
                continue

            # Build the url pattern
            regex = route.url.format(
                prefix=prefix,
                lookup=lookup,
                trailing_slash=self.trailing_slash,
            )

            # If there is no prefix, the first part of the url is probably
            #   controlled by project's urls.py and the router is in an app,
            #   so a slash in the beginning will (A) cause Django to give
            #   warnings and (B) generate URLS that will require using '//'.
            regex_start = regex[:2]
            if not prefix and regex_start == '^/':
                regex = f'^{regex_start}'

            initkwargs = route.initkwargs.copy()
            initkwargs.update({
                'basename': basename,
                'detail': route.detail,
            })

            view = viewset.as_view(mapping, **initkwargs)
            name = route.name.format(basename=basename)
            ret.append(re_path(regex, view, name=name))
        return ret


# Манкипатчим функцию по resolve extra actions

def _reverse(  # noqa: WPS211
    viewname,
    args=None,
    kwargs=None,
    request=None,
    format=None,  # noqa: WPS125
    **extra,
):
    """
    Same as `django.urls.reverse`.

    but optionally takes a request and returns a fully qualified URL,
    using the request to get the base URL.
    """
    if format is not None:
        kwargs = kwargs or {}
        kwargs['format'] = format
    try:
        # преднамерено заменяется django.conf.urls.url (WPS442)
        url = django_reverse(  # noqa: WPS442
            viewname, args=args, kwargs=kwargs, **extra,
        )
    except NoReverseMatch as exception:
        # Пытаемся получить reverse url с использование namespace
        if request and request._request.resolver_match.namespace:
            viewname = '{namespace}:{viewname}'.format(
                namespace=request._request.resolver_match.namespace,
                viewname=viewname,
            )
            url = django_reverse(  # noqa: WPS442
                viewname, args=args, kwargs=kwargs, **extra,
            )
        else:
            raise exception
    if request:
        return request.build_absolute_uri(url)
    return url


reverse._reverse = _reverse


class CustomAPIRootView(APIRootView):
    """Корневой элемент для роутера."""

    __doc__ = 'The root view for Custom API'
    name = _('Custom')


router = ApiRouter()
router.APIRootView = CustomAPIRootView
