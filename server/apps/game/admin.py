from django.contrib import admin
from server.apps.game.models import IncomeItem, UserIncomeItem, Promo


@admin.register(IncomeItem)
class IncomeItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'base_income', 'income_multiplier', 'price_multiplier', 'visible')
    search_fields = ('name',)


@admin.register(UserIncomeItem)
class UserIncomeItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'item', 'level')
    search_fields = ('user', 'item')


@admin.register(Promo)
class PromoAdmin(admin.ModelAdmin):
    list_display = ('name', 'reward', 'visible')
    search_fields = ('name',)
