import pytest
from django.urls import reverse
from rest_framework import status
from booking.models import Table, Reservation


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_authenticated, expected_status, error_message",
    [
        (
            False,
            status.HTTP_401_UNAUTHORIZED,
            "Authentication credentials were not provided",
        ),
        (
            True,
            status.HTTP_200_OK,
            None,
        ),
    ],
)
def test_reservation_list_access(
    api_client,
    create_user,
    is_authenticated,
    expected_status,
    error_message,
):
    if is_authenticated:
        user = create_user("test@example.com", "password", "testuser")
        api_client.force_authenticate(user=user)

    url = reverse("reservation-list")
    response = api_client.get(url)

    assert response.status_code == expected_status
    if not is_authenticated:
        detail = response.data.get("detail", "")
        assert error_message in detail


@pytest.mark.django_db
@pytest.mark.parametrize(
    "number_of_seats, expected_status",
    [
        (
            4,
            status.HTTP_201_CREATED,
        ),
    ],
)
def test_book_api_returns_reservation_details(
    api_client,
    create_user,
    number_of_seats,
    expected_status,
):
    user = create_user("test@example.com", "password", "testuser")
    api_client.force_authenticate(user=user)

    Table.objects.create(table_number=1, total_seats=6)

    payload = {"number_of_seats": number_of_seats}
    url = reverse("reservation-list")
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == expected_status
    data = response.data
    assert "cost" in data, "Cost field is missing in the response."
    assert "table" in data, "Table field is missing in the response."
    assert (
        "number_of_seats" in data
    ), "Number of seats field is missing in the response."
    assert (
        data["number_of_seats"] == number_of_seats
    ), "Number of seats does not match the input."


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_authenticated, expected_status, error_message",
    [
        (
            False,
            status.HTTP_401_UNAUTHORIZED,
            "Authentication credentials were not provided",
        ),
        (
            True,
            status.HTTP_200_OK,
            None,
        ),
    ],
)
def test_reservation_retrieve(
    api_client,
    create_user,
    is_authenticated,
    expected_status,
    error_message,
):
    user = create_user("test@example.com", "password", "testuser")
    if is_authenticated:
        api_client.force_authenticate(user=user)

    table = Table.objects.create(table_number=1, total_seats=6)
    reservation = Reservation.objects.create(
        user=user, table=table, number_of_seats=4, cost=33.33, active=True
    )

    url = reverse("reservation-detail", args=[reservation.id])
    response = api_client.get(url)

    assert response.status_code == expected_status
    if not is_authenticated:
        detail = response.data.get("detail", "")
        assert error_message in detail
    else:
        assert "table" in response.data
        assert "number_of_seats" in response.data
        assert "cost" in response.data
        assert response.data["table"] == table.id


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_authenticated, expected_status, error_message",
    [
        (
            False,
            status.HTTP_401_UNAUTHORIZED,
            "Authentication credentials were not provided",
        ),
        (
            True,
            status.HTTP_200_OK,
            None,
        ),
    ],
)
def test_reservation_update(
    api_client,
    create_user,
    is_authenticated,
    expected_status,
    error_message,
):
    user = create_user("test@example.com", "password", "testuser")
    if is_authenticated:
        api_client.force_authenticate(user=user)

    table = Table.objects.create(table_number=1, total_seats=6)
    reservation = Reservation.objects.create(
        user=user, table=table, number_of_seats=4, cost=33.33, active=True
    )

    payload = {"number_of_seats": 6}
    url = reverse("reservation-detail", args=[reservation.id])
    response = api_client.put(url, data=payload, format="json")

    assert response.status_code == expected_status
    if not is_authenticated:
        detail = response.data.get("detail", "")
        assert error_message in detail
    else:
        assert "number_of_seats" in response.data
        assert response.data["number_of_seats"] == 6


@pytest.mark.django_db
@pytest.mark.parametrize(
    "is_authenticated, expected_status, error_message",
    [
        (
            False,
            status.HTTP_401_UNAUTHORIZED,
            "Authentication credentials were not provided",
        ),
        (
            True,
            status.HTTP_200_OK,
            None,
        ),
    ],
)
def test_reservation_cancel(
    api_client,
    create_user,
    is_authenticated,
    expected_status,
    error_message,
):
    user = create_user("test@example.com", "password", "testuser")
    if is_authenticated:
        api_client.force_authenticate(user=user)

    table = Table.objects.create(table_number=1, total_seats=6)
    reservation = Reservation.objects.create(
        user=user, table=table, number_of_seats=4, cost=33.33, active=True
    )

    url = reverse("reservation-cancel", args=[reservation.id])
    response = api_client.post(url, format="json")

    assert response.status_code == expected_status
    if not is_authenticated:
        detail = response.data.get("detail", "")
        assert error_message in detail
    else:
        assert "message" in response.data
        assert response.data["message"] == "Reservation cancelled successfully."
