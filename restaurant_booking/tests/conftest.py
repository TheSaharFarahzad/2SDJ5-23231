import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def create_user(db):
    def _create_user(email, password, username, is_superuser=False, is_active=True):
        user = User.objects.create_user(
            username=username, email=email, password=password
        )
        user.is_active = is_active
        user.is_superuser = is_superuser
        user.save()
        return user

    return _create_user


@pytest.fixture
def obtain_token_url():
    return reverse("token_obtain_pair")


@pytest.fixture
def refresh_token_url():
    return reverse("token_refresh")


@pytest.fixture
def create_tokens(api_client, create_user):
    def _create_tokens(username, password):
        data = {"username": username, "password": password}
        response = api_client.post(reverse("token_obtain_pair"), data=data)
        return response

    return _create_tokens
