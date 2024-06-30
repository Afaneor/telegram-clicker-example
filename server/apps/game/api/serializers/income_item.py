from rest_framework.serializers import ModelSerializer

from server.apps.game.models.income_item import IncomeItem, UserIncomeItem


class UserIncomeItemSerializer(ModelSerializer):
    class Meta:
        model = UserIncomeItem
        fields = ('level', 'updated_at', 'created_at',)


class IncomeItemSerializer(ModelSerializer):

    user_item = UserIncomeItemSerializer(
        read_only=True,
        default=dict,
    )

    class Meta:
        model = IncomeItem
        fields = ('id', 'name', 'icon', 'base_price', 'base_income', 'income_multiplier', 'price_multiplier')
        read_only_fields = ('id',)
