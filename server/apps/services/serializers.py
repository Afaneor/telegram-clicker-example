from typing import Dict

from rest_framework import serializers
from rest_framework.fields import empty


class ModelSerializerWithPermission(serializers.ModelSerializer):
    """Базовый сериалайзер с логикой указания прав доступа к объекту."""

    permission_rules = serializers.SerializerMethodField()
    action_names: Dict[str, str] = {}

    def __init__(self, instance=None, data=empty, **kwargs):  # noqa: WPS110, E501
        """Устанавливаем начальные значения."""
        super().__init__(instance, data, **kwargs)
        self.action_names.update(
            {
                'add': 'add',
                'view': 'view',
                'delete': 'delete',
                'change': 'change',
                'list': 'list',
            },
        )

    def get_permission_rules(self, obj):  # noqa: WPS615, WPS110
        """Получение прав доступа к объекту."""
        if user := getattr(self.context.get('request'), 'user', None):
            obj_name = obj.__class__.__name__.lower()
            app_name = obj.__module__.split('.')[-3]

            return {
                action_name:
                    user.has_perm(f'{app_name}.{action}_{obj_name}', obj)
                for action_name, action in self.action_names.items()
            }

        return None
