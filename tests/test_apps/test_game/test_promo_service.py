import pytest

from server.apps.game.services.promo import AlreadyClaimedError


@pytest.mark.django_db
def test_claim(user, promo, promo_service):
    promo_service.claim(promo, user)
    assert promo.users_claimed.filter(id=user.id).exists()


@pytest.mark.django_db
def test_already_claimed(user, promo, promo_service):
    promo_service.claim(promo, user)
    with pytest.raises(AlreadyClaimedError):
        promo_service.claim(promo, user)


@pytest.mark.django_db
def test_promo_claim_update_balance(user, promo, promo_service):
    promo_service.claim(promo, user)
    user.refresh_from_db()
    assert user.balance == 100 + promo.reward
