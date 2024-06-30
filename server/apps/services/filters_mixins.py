import django_filters
from django.utils.translation import gettext_lazy as _
from django_filters.fields import MultipleChoiceField


class NonValidatingMultipleChoiceField(MultipleChoiceField):
    """Поле для множественного выбора данных без валидации."""

    def validate(self, value):  # noqa: WPS110
        """Отключение валидации, чтобы можно было передавать любые значения."""
        pass  # noqa: WPS420


class NonValidatingMultipleChoiceFilter(django_filters.MultipleChoiceFilter):
    """Фильтр для множественного выбора данных без валидации."""

    field_class = NonValidatingMultipleChoiceField


class CreatedUpdatedDateFilterMixin(django_filters.FilterSet):
    """Миксин для фильтрации по датам создания и обновления."""

    created_at_date = django_filters.DateFromToRangeFilter(
        field_name='created_at__date',
        label=_('Фильтрация по дате создания'),
    )

    updated_at_date = django_filters.DateFromToRangeFilter(
        field_name='updated_at__date',
        label=_('Фильтрация по дате изменения'),
    )


class UserFilterMixin(django_filters.FilterSet):
    """Миксин для фильтрации по пользователю."""

    user_email = django_filters.CharFilter(
        field_name='user__email',
        lookup_expr='icontains',
        label=_('Фильтрация по email пользователя'),
    )
    user_username = django_filters.CharFilter(
        field_name='user__username',
        lookup_expr='icontains',
        label=_('Фильтрация по username пользователя'),
    )
    user_first_name = django_filters.CharFilter(
        field_name='user__first_name',
        lookup_expr='icontains',
        label=_('Фильтрация по имени пользователя'),
    )
    user_last_name = django_filters.CharFilter(
        field_name='user__last_name',
        lookup_expr='icontains',
        label=_('Фильтрация по фамилии пользователя'),
    )
    user_middle_name = django_filters.CharFilter(
        field_name='user__middle_name',
        lookup_expr='icontains',
        label=_('Фильтрация по отчеству пользователя'),
    )
