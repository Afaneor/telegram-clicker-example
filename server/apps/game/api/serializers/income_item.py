from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from server.apps.game.models.income_item import IncomeItem, UserIncomeItem


class UserIncomeItemSerializer(ModelSerializer):
    class Meta:
        model = UserIncomeItem
        fields = ('level', 'updated_at', 'created_at',)


class IncomeItemSerializer(ModelSerializer):

    user_item = SerializerMethodField()

    class Meta:
        model = IncomeItem
        fields = (
            'id',
            'name',
            'icon',
            'base_price',
            'base_income',
            'income_multiplier',
            'price_multiplier',
            'user_item',
        )
        read_only_fields = ('id',)

    def get_user_item(self, obj):
        user_item = getattr(obj, 'user_item', [])
        if user_item:
            return UserIncomeItemSerializer(user_item[0]).data
        return {}
