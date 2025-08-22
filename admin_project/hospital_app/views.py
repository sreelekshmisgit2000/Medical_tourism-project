from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import *
from .serializers import *


class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer


class TreatmentCategoryViewSet(viewsets.ModelViewSet):
    queryset = TreatmentCategory.objects.all()
    serializer_class = TreatmentCategorySerializer


class AlliedServiceViewSet(viewsets.ModelViewSet):
    queryset = AlliedService.objects.all()
    serializer_class = AlliedServiceSerializer


class AccreditationViewSet(viewsets.ModelViewSet):
    queryset = Accreditation.objects.all()
    serializer_class = AccreditationSerializer


class TreatmentScheduleViewSet(viewsets.ModelViewSet):
    queryset = TreatmentSchedule.objects.all()
    serializer_class = TreatmentScheduleSerializer


class TreatmentEquipmentViewSet(viewsets.ModelViewSet):
    queryset = TreatmentEquipment.objects.all()
    serializer_class = TreatmentEquipmentSerializer


class ServiceScheduleViewSet(viewsets.ModelViewSet):
    queryset = ServiceSchedule.objects.all()
    serializer_class = ServiceScheduleSerializer


class AccreditationRenewalViewSet(viewsets.ModelViewSet):
    queryset = AccreditationRenewal.objects.all()
    serializer_class = AccreditationRenewalSerializer