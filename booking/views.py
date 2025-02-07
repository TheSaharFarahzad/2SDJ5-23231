from rest_framework import permissions, viewsets, status
from rest_framework.exceptions import ValidationError as DRFValidationError
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError as DjangoValidationError

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
            raise DRFValidationError("Cannot create more than 10 tables.")
        try:
            serializer.save()
        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)


class ReservationViewSet(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Reservation.objects.all()
        if self.action == "cancel":
            return queryset.select_related("user", "table")
        return queryset.filter(user=self.request.user).select_related("table")

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return ReservationListSerializer
        return ReservationCreateSerializer

    def validate_cancel_request(self, reservation, user):
        if reservation.user != user:
            raise DRFValidationError("You can only cancel your own reservations.")
        if not reservation.active:
            raise DRFValidationError("This reservation is already cancelled.")

    @action(detail=True, methods=["post"], name="cancel")
    def cancel(self, request, pk=None):
        try:
            reservation = self.get_object()
        except Reservation.DoesNotExist:
            return Response(
                {"detail": "Reservation not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            self.validate_cancel_request(reservation, request.user)
        except DRFValidationError as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )

        reservation.active = False
        reservation.save()

        return Response(
            {"message": "Reservation cancelled successfully."},
            status=status.HTTP_200_OK,
        )

    def perform_create(self, serializer):
        try:
            number_of_seats = Reservation.validate_number_of_seats(
                self.request.data.get("number_of_seats")
            )
            best_table = Table.objects.get_best_available_table(number_of_seats)
            cost = best_table.calculate_cost(number_of_seats)
        except DjangoValidationError as e:
            raise DRFValidationError(e.messages)

        reservation = serializer.save(
            user=self.request.user,
            table=best_table,
            cost=cost,
            active=True,
        )

        response_data = {
            "table": TableSerializer(reservation.table).data,
            "number_of_seats": reservation.number_of_seats,
            "cost": str(reservation.cost),
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
