from rest_framework import serializers
from .models import Reservation, Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class ReservationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = [
            "id",
            "user",
            "table",
            "number_of_seats",
            "cost",
            "booked_at",
            "active",
        ]


class ReservationCreateSerializer(serializers.ModelSerializer):
    cost = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)
    table = TableSerializer(read_only=True)

    class Meta:
        model = Reservation
        fields = ["number_of_seats", "cost", "table"]
