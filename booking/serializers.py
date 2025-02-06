from rest_framework import serializers
from .models import Reservation, Table


class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = "__all__"


class ReservationListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["user", "table", "number_of_seats", "cost", "booked_at", "active"]


class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["number_of_seats"]
