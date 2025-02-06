from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import (
    ReservationListSerializer,
    ReservationCreateSerializer,
    TableSerializer,
)
from .models import Reservation, Table


class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        if Table.objects.count() >= 10:
            raise ValidationError("Cannot create more than 10 tables.")
        serializer.save()


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReservationListSerializer
        return ReservationCreateSerializer

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        if reservation.user != request.user:
            raise ValidationError("You can only cancel your own reservations.")

        reservation.active = False
        reservation.save()
        return Response(
            {"message": "Reservation cancelled successfully."},
            status=status.HTTP_200_OK,
        )

    def get_valid_number_of_seats(self):
        number_of_seats = self.request.data.get("number_of_seats")

        if number_of_seats is None:
            raise ValidationError("Number of seats is required.")

        try:
            number_of_seats = int(number_of_seats)
        except ValueError:
            raise ValidationError("Invalid number of seats.")

        if number_of_seats < 4:
            raise ValidationError("Number of seats must be at least 4.")

        if number_of_seats % 2 != 0:
            number_of_seats += 1

        return number_of_seats

    def get_best_available_table(self, number_of_seats):
        available_tables = Table.objects.filter(
            total_seats__gte=number_of_seats
        ).order_by("price", "total_seats")

        if not available_tables.exists():
            raise ValidationError("No available table for this number of seats.")

        return available_tables.first()

    def calculate_cost(self, table, number_of_seats):
        seat_price = table.price / table.total_seats
        total_seat_cost = number_of_seats * seat_price

        if number_of_seats == table.total_seats:
            return (table.total_seats - 1) * seat_price

        return total_seat_cost

    def perform_create(self, serializer):
        number_of_seats = self.get_valid_number_of_seats()
        best_table = self.get_best_available_table(number_of_seats)

        cost = self.calculate_cost(best_table, number_of_seats)

        reservation = serializer.save(
            user=self.request.user,
            table=best_table,
            cost=cost,
            active=True,
        )

        response_serializer = ReservationListSerializer(reservation)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
