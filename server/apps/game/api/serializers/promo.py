from rest_framework.serializers import ModelSerializer

from server.apps.game.models import Promo


class PromoSerializer(ModelSerializer):
    class Meta:
        model = Promo
        fields = '__all__'
