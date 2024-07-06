from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from server.apps.game.models import Promo


class PromoSerializer(ModelSerializer):
    claimed = serializers.BooleanField(read_only=True)

    class Meta:
        model = Promo
        fields = ('id', 'name', 'reward', 'claimed')
