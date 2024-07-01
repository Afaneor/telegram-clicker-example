import pytest
from model_bakery import baker

from server.apps.game.services.income_item import IncomeItemService
from server.apps.game.services.promo import PromoService


@pytest.fixture
def user():
    return baker.make('user.User', balance=100)


@pytest.fixture
def user_income_item(user, income_item):
    return baker.make('game.UserIncomeItem', user=user, item=income_item, level=1)


@pytest.fixture
def promo():
    return baker.make('game.Promo')


@pytest.fixture
def income_item():
    return baker.make(
        'game.IncomeItem',
        base_price=100,
        base_income=1,
        price_multiplier=2,
    )


@pytest.fixture
def income_item_service():
    return IncomeItemService()


@pytest.fixture
def promo_service():
    return PromoService()
