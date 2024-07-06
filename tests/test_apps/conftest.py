import pytest
from model_bakery import baker
from rest_framework.fields import DateTimeField

from server.apps.game.services.income_item import IncomeItemService
from server.apps.game.services.promo import PromoService
import faker

fake = faker.Faker()

@pytest.fixture
def create_user():
    def factory(**kwargs):
        return baker.make('user.User', balance=100, username=fake.user_name, **kwargs)
    return factory


@pytest.fixture
def create_user_income_item(create_user, create_income_item):
    def factory(**kwargs):
        user = create_user()
        item = create_income_item()
        return baker.make('game.UserIncomeItem', user=user, item=item, level=1, **kwargs)
    return factory


@pytest.fixture
def user_income_item(create_user, create_income_item):
    user = create_user()
    item = create_income_item()
    return baker.make('game.UserIncomeItem', user=user, item=item, level=1)


@pytest.fixture
def create_promo():
    def factory(**kwargs):
        return baker.make('game.Promo', visible=True, **kwargs)
    return factory


@pytest.fixture
def create_income_item():
    def factory(**kwargs):
        return baker.make(
            'game.IncomeItem',
            name=fake.word(),
            base_price=100,
            base_income=1,
            price_multiplier=2,
            visible=True,
            **kwargs,
        )
    return factory


@pytest.fixture
def format_income_item():
    def _format(income_item, user_income_item=None):
        if user_income_item is None:
            user_item = {}
        else:
            user_item = {
                'level': user_income_item.level,
                'updated_at': DateTimeField().to_representation(user_income_item.updated_at),
                'created_at': DateTimeField().to_representation(user_income_item.created_at),
            }

        return {
            'id': income_item.id,
            'name': income_item.name,
            'icon': income_item.icon.url if income_item.icon else None,
            'base_price': income_item.base_price,
            'base_income': income_item.base_income,
            'income_multiplier': income_item.income_multiplier,
            'price_multiplier': float(income_item.price_multiplier),
            'user_item': user_item,
        }

    return _format


@pytest.fixture
def income_item_service():
    return IncomeItemService()


@pytest.fixture
def promo_service():
    return PromoService()
