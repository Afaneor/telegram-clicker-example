from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from server.apps.user.models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    """Класс админки пользователя."""

    list_display = (
        'id',
        'email',
        'username',
        'last_name',
        'first_name',
        'is_superuser',
    )
    search_fields = (
        'last_name',
        'first_name',
        'username',
        'email',
    )
    list_filter = ('is_superuser', 'is_active')
    ordering = (
        '-id',
    )
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('avatar', 'first_name', 'last_name', 'email')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                    'groups',
                    'user_permissions',
                ),
            },
        ),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('username', 'password1', 'password2', 'email'),
            },
        ),
    )
