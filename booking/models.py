from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.conf import settings

User = get_user_model()


class TableManager(models.Manager):
    def get_best_available_table(self, number_of_seats):
        available_tables = self.filter(total_seats__gte=number_of_seats).order_by(
            "price", "total_seats"
        )
        if not available_tables.exists():
            raise ValidationError("No available table for this number of seats.")
        return available_tables.first()


class Table(models.Model):
    table_number = models.PositiveSmallIntegerField(unique=True)
    total_seats = models.PositiveSmallIntegerField()
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=settings.DEFAULT_TABLE_PRICE
    )

    objects = TableManager()

    def clean(self):
        if self.total_seats < 4 or self.total_seats > 10:
            raise ValidationError("Total seats must be between 4 and 10.")

    def calculate_cost(self, number_of_seats):
        seat_price = self.price / self.total_seats
        total_seat_cost = number_of_seats * seat_price

        if number_of_seats == self.total_seats:
            return (self.total_seats - 1) * seat_price

        return total_seat_cost

    def __str__(self):
        return f"Table {self.table_number} ({self.total_seats} seats)"


class Reservation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    table = models.ForeignKey(
        Table, on_delete=models.CASCADE, related_name="reservations"
    )
    number_of_seats = models.PositiveSmallIntegerField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    booked_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    @classmethod
    def validate_number_of_seats(cls, number_of_seats):
        if number_of_seats < 4:
            raise ValidationError("Number of seats must be at least 4.")
        if number_of_seats % 2 != 0:
            number_of_seats += 1
        return number_of_seats

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.number_of_seats} seats at Table {self.table.table_number}"
