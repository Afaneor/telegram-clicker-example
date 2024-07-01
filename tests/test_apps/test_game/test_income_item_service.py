import pytest
from server.apps.game.models import UserIncomeItem
from server.apps.game.services.errors import AlreadyBoughtError, NotEnoughMoneyError, NoItemForUserError


@pytest.mark.django_db
def test_buy_item_success(income_item_service, user, income_item):
    income_item_service.buy(income_item, user)
    assert UserIncomeItem.objects.filter(user=user, item=income_item).exists()


@pytest.mark.django_db
def test_buy_item_already_bought(income_item_service, user, income_item):
    UserIncomeItem.objects.create(user=user, item=income_item, level=1)
    with pytest.raises(AlreadyBoughtError):
        income_item_service.buy(income_item, user)


@pytest.mark.django_db
def test_buy_item_not_enough_money(income_item_service, user, income_item):
    user.balance = 50
    user.save()
    with pytest.raises(NotEnoughMoneyError):
        income_item_service.buy(income_item, user)


@pytest.mark.django_db
def test_upgrade_item_success(income_item_service, user, income_item):
    income_item_service.buy(user=user, income_item=income_item)
    user.balance = 1000
    user.save()
    income_item_service.upgrade(income_item, user)
    user_item = UserIncomeItem.objects.get(user=user, item=income_item)
    assert user_item.level == 2


@pytest.mark.django_db
def test_upgrade_item_no_item(income_item_service, user, income_item):
    with pytest.raises(NoItemForUserError):
        income_item_service.upgrade(income_item, user)


@pytest.mark.django_db
def test_upgrade_item_not_enough_money(income_item_service, user, income_item):
    UserIncomeItem.objects.create(user=user, item=income_item, level=1)
    user.balance = 50
    user.save()
    with pytest.raises(NotEnoughMoneyError):
        income_item_service.upgrade(income_item, user)
