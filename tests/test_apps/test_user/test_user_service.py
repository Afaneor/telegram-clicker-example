from datetime import datetime, timedelta
from unittest.mock import patch

import pytest

from server.apps.user.services.user import UserService


@pytest.mark.django_db
def test_get_user_available_balance_with_no_income_items(user_income_item):
    user = user_income_item.user
    balance = UserService.get_user_available_balance(user)
    assert balance == 100


@patch('datetime.datetime')
@pytest.mark.django_db
def test_get_user_available_balance_with_income_items(mock_datetime, user_income_item):
    # подменяем текущее время
    mock_datetime.utcnow.return_value = datetime(2022, 1, 1, 12, 0, 0)
    user = user_income_item.user
    # подставляем, как будто последнее обновление было 15 минут назад
    user.last_balance_update = int((datetime.utcnow() - timedelta(seconds=900)).timestamp())

    balance = UserService.get_user_available_balance(user)

    assert balance == 1000
    assert user.last_claimed == int(datetime.utcnow().timestamp())
