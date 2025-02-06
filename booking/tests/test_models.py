import pytest
from django.core.exceptions import ValidationError
from booking.models import Table


@pytest.mark.django_db
@pytest.mark.parametrize(
    "table_number, total_seats, should_raise",
    [
        (1, 6, False),
        (1, 3, True),
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
