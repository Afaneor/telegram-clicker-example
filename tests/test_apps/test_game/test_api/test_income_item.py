from time import sleep

import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_get_income_item_without_bought_items(
    api_client,
    create_user,
    create_income_item,
    format_income_item
):
    user = create_user()
    income_item = create_income_item()

    api_client.force_authenticate(user)
    response = api_client.get(reverse('api:game:income-items-list'))

    assert response.status_code == 200
    assert response.data == [
        format_income_item(income_item),
    ]


@pytest.mark.django_db
def test_get_income_item_with_single_bought(
    api_client,
    create_user,
    create_income_item,
    format_income_item
):
    user = create_user()
    income_item = create_income_item()
    user_income_item = user.user_income_items.create(item=income_item, level=1)

    api_client.force_authenticate(user)
    response = api_client.get(reverse('api:game:income-items-list'))

    assert response.status_code == 200
    assert response.data == [
        format_income_item(income_item, user_income_item),
    ]


@pytest.mark.django_db
def test_get_income_item_bought_multiple_items(
    api_client,
    create_user,
    create_income_item,
    format_income_item,
):
    """
    Test when user have multiple items nothing will break.
    """
    user = create_user()
    first_income_item = create_income_item()
    second_income_item = create_income_item()
    first_user_income_item = user.user_income_items.create(item=first_income_item, level=1)
    second_user_income_item = user.user_income_items.create(item=second_income_item, level=1)

    api_client.force_authenticate(user)
    response = api_client.get(reverse('api:game:income-items-list'))

    assert response.status_code == 200
    assert response.data == [
        format_income_item(first_income_item, first_user_income_item),
        format_income_item(second_income_item, second_user_income_item),
    ]
