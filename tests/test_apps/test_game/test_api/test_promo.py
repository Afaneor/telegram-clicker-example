import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_get_promo(
    api_client,
    create_user,
    create_promo,
):
    user = create_user()
    promo = create_promo()
    api_client.force_authenticate(user)
    response = api_client.get(reverse('api:game:promos-list'))
    assert response.status_code == 200
    assert response.data == [
        {
            'id': promo.id,
            'name': promo.name,
            'reward': promo.reward,
            'claimed': False,
        },
    ]


@pytest.mark.django_db
def test_claim_promo(
    api_client,
    create_user,
    create_promo,
):
    user = create_user()
    promo = create_promo()
    api_client.force_authenticate(user)
    response = api_client.post(reverse('api:game:promos-claim', kwargs={'pk': promo.id}))
    assert response.status_code == 200
    assert user.promos_claimed.filter(pk=promo.id).exists()


@pytest.mark.django_db
def test_get_claimed_promo(
    api_client,
    create_user,
    create_promo,
):
    user = create_user()
    promo = create_promo()
    user.promos_claimed.add(promo)
    api_client.force_authenticate(user)
    response = api_client.get(reverse('api:game:promos-list'))
    assert response.status_code == 200
    assert response.data == [
        {
            'id': promo.id,
            'name': promo.name,
            'reward': promo.reward,
            'claimed': True,
        },
    ]
