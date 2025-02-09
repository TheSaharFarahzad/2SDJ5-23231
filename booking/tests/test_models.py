import pytest
from django.core.exceptions import ValidationError
from booking.models import Reservation, Table


@pytest.mark.parametrize(
    "input_seats, expected_output, expect_error",
    [
        (0, None, True),
        (1, 2, False),
        (2, 2, False),
        (3, 4, False),
        (4, 4, False),
        (5, 6, False),
        (6, 6, False),
        (7, 8, False),
        (8, 8, False),
        (9, 10, False),
        (10, 10, False),
    ],
)
def test_validate_number_of_seats(input_seats, expected_output, expect_error):
    if expect_error:
        with pytest.raises(ValidationError):
            Reservation.validate_number_of_seats(input_seats)
    else:
        assert Reservation.validate_number_of_seats(input_seats) == expected_output


@pytest.mark.django_db
def test_get_best_available_table():
    Table.objects.create(table_number=1, total_seats=4, price=100)
    Table.objects.create(table_number=2, total_seats=6, price=80)
    Table.objects.create(table_number=3, total_seats=6, price=90)

    best_table = Table.objects.get_best_available_table(4)
    assert best_table.table_number == 2

    with pytest.raises(ValidationError):
        Table.objects.get_best_available_table(12)


@pytest.mark.parametrize(
    "total_seats, price, requested_seats, expected_cost",
    [
        (4, 100, 4, 75),
        (4, 100, 2, 50),
        (6, 120, 6, 100),
        (6, 120, 4, 80),
    ],
)
def test_calculate_cost(total_seats, price, requested_seats, expected_cost):
    table = Table(total_seats=total_seats, price=price)
    assert table.calculate_cost(requested_seats) == expected_cost


@pytest.mark.django_db
@pytest.mark.parametrize(
    "table_number, total_seats, should_raise",
    [
        (1, 3, True),
        (1, 4, False),
        (1, 6, False),
        (1, 10, False),
        (1, 11, True),
    ],
)
def test_table_seat_validation(
    table_number,
    total_seats,
    should_raise,
):
    table = Table(
        table_number=table_number,
        total_seats=total_seats,
    )

    if should_raise:
        with pytest.raises(ValidationError):
            table.full_clean()
    else:
        try:
            table.full_clean()
        except ValidationError:
            pytest.fail("ValidationError raised unexpectedly!")
