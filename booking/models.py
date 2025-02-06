from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Table(models.Model):
    table_number = models.PositiveSmallIntegerField(unique=True)
    total_seats = models.PositiveSmallIntegerField()

    def clean(self):
        if self.total_seats < 4 or self.total_seats > 10:
            raise ValidationError("Total seats must be between 4 and 10.")

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

    def __str__(self):
        return f"Reservation by {self.user.username} for {self.number_of_seats} seats at Table {self.table.table_number}"
