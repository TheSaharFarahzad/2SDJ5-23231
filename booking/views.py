from rest_framework import permissions, viewsets
from rest_framework.exceptions import ValidationError
from .serializers import ReservationSerializer, TableSerializer
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
    serializer_class = ReservationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Reservation.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
