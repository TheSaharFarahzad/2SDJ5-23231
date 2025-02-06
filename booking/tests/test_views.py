import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from django.urls import reverse
from booking.models import Table

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
):

    user = User.objects.create_user(username="testuser", password="password")
    client = APIClient()
    client.force_authenticate(user=user)

    for i in range(table_count):
        Table.objects.create(table_number=i + 1, total_seats=6)

    url = reverse("table-list")
    data = {"table_number": table_number, "total_seats": 6}
    response = client.post(url, data)
    detail_message = get_detail_message(response.data)

    assert response.status_code == expected_status_code
    if expected_message:
        assert detail_message == expected_message
    else:
        assert response.data["table_number"] == table_number
        assert response.data["total_seats"] == 6
