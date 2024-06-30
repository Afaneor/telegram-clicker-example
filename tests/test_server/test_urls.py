import pytest
from django.test import Client
from rest_framework import status


@pytest.mark.django_db()
def test_health_check(client: Client) -> None:
    """This test ensures that health check is accessible."""
    response = client.get('/health/')

    assert response.status_code == status.HTTP_200_OK


def test_admin_unauthorized(client: Client) -> None:
    """This test ensures that admin panel requires auth."""
    response = client.get('/admin/')

    assert response.status_code == status.HTTP_302_FOUND


def test_admin_authorized(admin_client: Client) -> None:
    """This test ensures that admin panel is accessible."""
    response = admin_client.get('/admin/')

    assert response.status_code == status.HTTP_200_OK


def test_admin_docs_unauthorized(client: Client) -> None:
    """This test ensures that admin panel docs requires auth."""
    response = client.get('/admin/doc/')

    assert response.status_code == status.HTTP_302_FOUND


def test_admin_docs_authorized(admin_client: Client) -> None:
    """This test ensures that admin panel docs are accessible."""
    response = admin_client.get('/admin/doc/')

    assert response.status_code == status.HTTP_200_OK
    assert b'docutils' not in response.content


def test_robots_txt(client: Client) -> None:
    """This test ensures that `robots.txt` is accessible."""
    response = client.get('/robots.txt')

    assert response.status_code == status.HTTP_200_OK
    assert response.get('Content-Type') == 'text/plain'


def test_humans_txt(client: Client) -> None:
    """This test ensures that `humans.txt` is accessible."""
    response = client.get('/humans.txt')

    assert response.status_code == status.HTTP_200_OK
    assert response.get('Content-Type') == 'text/plain'
