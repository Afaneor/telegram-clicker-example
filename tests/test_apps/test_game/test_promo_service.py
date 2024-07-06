import pytest

from server.apps.game.services.promo import AlreadyClaimedError


@pytest.mark.django_db
def test_claim(create_user, create_promo, promo_service):
    user = create_user()
    promo = create_promo()
    promo_service.claim(promo, user)
    assert promo.users_claimed.filter(id=user.id).exists()


@pytest.mark.django_db
def test_already_claimed(create_user, create_promo, promo_service):
    user = create_user()
    promo = create_promo()
    promo_service.claim(promo, user)
    with pytest.raises(AlreadyClaimedError):
        promo_service.claim(promo, user)


@pytest.mark.django_db
def test_promo_claim_update_balance(create_user, create_promo, promo_service):
    user = create_user()
    promo = create_promo()
    promo_service.claim(promo, user)
    user.refresh_from_db()
    assert user.balance == 100 + promo.reward
