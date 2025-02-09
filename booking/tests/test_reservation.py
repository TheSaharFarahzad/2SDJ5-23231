import pytest
from rest_framework import status
from django.urls import reverse
from booking.models import Table, Reservation


@pytest.fixture
def create_tables():
    return [
        Table.objects.create(table_number=1, total_seats=4, price=100),
        Table.objects.create(table_number=2, total_seats=6, price=150),
        Table.objects.create(table_number=3, total_seats=8, price=200),
        Table.objects.create(table_number=4, total_seats=10, price=250),
    ]


@pytest.mark.django_db
@pytest.mark.parametrize(
    "requested_seats, expected_table_number, expected_cost",
    [
        (4, 1, "75.00"),  # 3 → 4
        (4, 1, "75.00"),
        (6, 2, "125.00"),  # 5 → 6
        (6, 2, "125.00"),
        (8, 3, "175.00"),  # 7 → 8
        (8, 3, "175.00"),
        (10, 4, "225.00"),
    ],
)
def test_reservation_booking(
    api_client,
    create_user,
    create_tables,
    requested_seats,
    expected_table_number,
    expected_cost,
):
    user = create_user(
        email="test@example.com",
        password="testpass",
        username="testuser",
    )
    api_client.force_authenticate(user=user)

    url = reverse("reservation-list")
    data = {"number_of_seats": requested_seats}
    response = api_client.post(url, data=data, format="json")
    assert response.status_code == status.HTTP_201_CREATED

    reservation = Reservation.objects.filter(user=user).latest("id")
    assert reservation.table.table_number == expected_table_number
    assert str(reservation.cost) == expected_cost


@pytest.mark.django_db
@pytest.mark.parametrize(
    "invalid_seat_count, expected_error",
    [
        (2, None),
        (5, None),
        (7, None),
    ],
)
def test_reservation_invalid_seats(
    api_client,
    create_user,
    create_tables,
    invalid_seat_count,
    expected_error,
):
    user = create_user(
        email="test@example.com",
        password="testpass",
        username="testuser",
    )
    api_client.force_authenticate(user=user)

    url = reverse("reservation-list")
    data = {"number_of_seats": invalid_seat_count}
    response = api_client.post(url, data=data, format="json")

    if expected_error:
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert expected_error in str(response.data)
    else:
        assert response.status_code == status.HTTP_201_CREATED


@pytest.mark.django_db
def test_reservation_no_available_table(api_client, create_user, create_tables):
    user = create_user(
        email="test@example.com",
        password="testpass",
        username="testuser",
    )
    api_client.force_authenticate(user=user)

    url = reverse("reservation-list")
    data = {"number_of_seats": 12}
    response = api_client.post(url, data=data, format="json")

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "No available table" in str(response.data)


@pytest.mark.django_db
def test_reservation_cancel(api_client, create_user, create_tables):
    user = create_user(
        email="test@example.com", password="testpass", username="testuser"
    )
    api_client.force_authenticate(user=user)

    table = create_tables[0]
    reservation = Reservation.objects.create(
        user=user, table=table, number_of_seats=4, cost=50
    )
    url = reverse("reservation-cancel", args=[reservation.id])
    response = api_client.post(url, format="json")

    assert response.status_code == status.HTTP_200_OK
    reservation.refresh_from_db()
    assert reservation.active is False
