from datetime import timedelta

import jwt
import pytest
from rest_framework import status

from django.conf import settings
from django.urls import reverse
from django.utils import timezone


@pytest.mark.django_db
@pytest.mark.parametrize(
    "username,password,expected_status,expected_keys",
    [
        (
            "normal_user",
            "testpassword",
            status.HTTP_200_OK,
            {"access", "refresh"},
        ),
        (
            "super_user",
            "testpassword",
            status.HTTP_200_OK,
            {"access", "refresh"},
        ),
        (
            "non_existing_user",
            "testpassword",
            status.HTTP_401_UNAUTHORIZED,
            set(),
        ),
        (
            "normal_user",
            "wrongpassword",
            status.HTTP_401_UNAUTHORIZED,
            set(),
        ),
    ],
)
def test_obtain_token(
    api_client,
    create_user,
    username,
    password,
    expected_status,
    expected_keys,
):
    create_user(
        email="normal_user@test.com",
        username="normal_user",
        password="testpassword",
    )

    create_user(
        email="super_user@test.com",
        username="super_user",
        password="testpassword",
        is_superuser=True,
    )

    url = reverse("token_obtain_pair")
    data = {"username": username, "password": password}
    response = api_client.post(url, data=data)
    assert response.status_code == expected_status
    assert set(response.data.keys()) >= expected_keys


@pytest.mark.django_db
@pytest.mark.parametrize(
    "refresh_token,expected_status,expected_keys",
    [
        (
            "valid_refresh_token",
            status.HTTP_200_OK,
            {"access"},
        ),
        (
            "invalid_refresh_token",
            status.HTTP_401_UNAUTHORIZED,
            set(),
        ),
        (
            "expired_refresh_token",
            status.HTTP_401_UNAUTHORIZED,
            set(),
        ),
    ],
)
def test_refresh_token(
    api_client,
    create_user,
    refresh_token,
    expected_status,
    expected_keys,
    obtain_token_url,
    refresh_token_url,
):
    user = create_user(
        email="user@test.com",
        username="testuser",
        password="testpassword",
    )

    if refresh_token == "valid_refresh_token":
        token_response = api_client.post(
            obtain_token_url, data={"username": "testuser", "password": "testpassword"}
        )
        refresh_token = token_response.data["refresh"]

    elif refresh_token == "expired_refresh_token":
        refresh_token = jwt.encode(
            {
                "user_id": user.id,
                "exp": timezone.now() - timedelta(seconds=1),
            },
            settings.SECRET_KEY,
            algorithm="HS256",
        )

    data = {"refresh": refresh_token}
    response = api_client.post(refresh_token_url, data=data)
    assert response.status_code == expected_status
    assert set(response.data.keys()) >= expected_keys
