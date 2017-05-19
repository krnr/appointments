from rest_framework import mixins, viewsets
from rest_framework.permissions import AllowAny

from .models import Appointment
from .serializers import AppointmentSerializer


class AppointmentViewSet(mixins.CreateModelMixin, 
                         viewsets.ReadOnlyModelViewSet):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = (AllowAny, )
