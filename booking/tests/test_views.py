import pytest
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from booking.models import Reservation, Table


User = get_user_model()


def get_detail_message(response_data):
    if isinstance(response_data, dict):
        return response_data.get("detail")
    elif isinstance(response_data, list):
        return response_data[0]
    return None


@pytest.mark.django_db
@pytest.mark.parametrize(
    "table_count, table_number, expected_status_code, expected_message",
    [
        (
            10,
            11,
            status.HTTP_400_BAD_REQUEST,
            "Cannot create more than 10 tables.",
        ),
        (
            9,
            10,
            status.HTTP_201_CREATED,
            None,
        ),
        (
            0,
            1,
            status.HTTP_201_CREATED,
            None,
        ),
    ],
)
def test_create_table(
    table_count,
    table_number,
    expected_status_code,
    expected_message,
    create_user,
    api_client,
):
    user = create_user("test@example.com", "password", "testuser")
    api_client.force_authenticate(user=user)

    for i in range(table_count):
        Table.objects.create(table_number=i + 1, total_seats=6)

    url = reverse("table-list")
    data = {"table_number": table_number, "total_seats": 6}
    response = api_client.post(url, data, format="json")
    detail_message = get_detail_message(response.data)

    assert response.status_code == expected_status_code
    if expected_message:
        assert expected_message in detail_message
    else:
        assert response.data["table_number"] == table_number
        assert response.data["total_seats"] == 6


@pytest.mark.django_db
@pytest.mark.parametrize(
    "number_of_seats, expected_status, expected_error_message",
    [
        (
            4,
            status.HTTP_201_CREATED,
            None,
        ),
        (
            0,
            status.HTTP_400_BAD_REQUEST,
            "Number of seats must be at least 4.",
        ),
    ],
)
def test_create_reservation_parametrized(
    api_client,
    create_user,
    number_of_seats,
    expected_status,
    expected_error_message,
):

    user = create_user("test@example.com", "password", "testuser")
    api_client.force_authenticate(user=user)

    if expected_status == status.HTTP_201_CREATED:
        Table.objects.create(table_number=1, total_seats=6)

    url = reverse("reservation-list")
    payload = {"number_of_seats": number_of_seats}
    response = api_client.post(url, data=payload, format="json")

    assert response.status_code == expected_status

    if expected_status == status.HTTP_201_CREATED:
        reservation = Reservation.objects.filter(user=user).first()
        assert reservation is not None, "Reservation was not created in the database."
        assert (
            reservation.number_of_seats == number_of_seats
        ), "Number of seats does not match."
        assert (
            reservation.active is True
        ), "Reservation should be active after creation."

    else:
        assert (
            expected_error_message in response.data
        ), "Expected error message not found in response."


@pytest.mark.django_db
@pytest.mark.parametrize(
    "reservation_active, request_username, expected_status, expected_error_message",
    [
        (
            True,
            "testuser",
            status.HTTP_200_OK,
            None,
        ),
        (
            True,
            "otheruser",
            status.HTTP_400_BAD_REQUEST,
            "You can only cancel your own reservations.",
        ),
        (
            False,
            "testuser",
            status.HTTP_400_BAD_REQUEST,
            "This reservation is already cancelled.",
        ),
    ],
)
def test_cancel_reservation(
    api_client,
    create_user,
    reservation_active,
    request_username,
    expected_status,
    expected_error_message,
):

    owner = create_user("owner@example.com", "password", "testuser")
    other = create_user("other@example.com", "password", "otheruser")
    request_user = owner if request_username == "testuser" else other

    table = Table.objects.create(table_number=1, total_seats=6)

    reservation = Reservation.objects.create(
        user=owner,
        table=table,
        cost=100,
        active=reservation_active,
        number_of_seats=4,
    )

    url = reverse("reservation-cancel", args=[reservation.id])
    api_client.force_authenticate(user=request_user)
    response = api_client.post(url, format="json")

    assert response.status_code == expected_status
    if expected_status == status.HTTP_400_BAD_REQUEST:
        detail = get_detail_message(response.data)
        assert expected_error_message in detail
    else:
        assert response.data.get("message") == "Reservation cancelled successfully."
        reservation.refresh_from_db()
        assert reservation.active is False
