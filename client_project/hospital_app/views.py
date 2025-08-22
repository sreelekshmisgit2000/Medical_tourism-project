from django.shortcuts import render
from rest_framework import generics
from .models import Hospital
from .serializers import HospitalSerializer
from .models import BestSurgeon, BestTreatment
from .serializers import BestSurgeonSerializer, BestTreatmentSerializer

# Create your views here.

class HospitalListCreateView(generics.ListCreateAPIView):
    queryset = Hospital.objects.all()  # type: ignore
    serializer_class = HospitalSerializer

class HospitalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Hospital.objects.all()  # type: ignore
    serializer_class = HospitalSerializer


class BestSurgeonListView(generics.ListAPIView):
    serializer_class = BestSurgeonSerializer

    def get_queryset(self):
        hospital_id = self.kwargs.get('hospital_id')
        if hospital_id:
            return BestSurgeon.objects.filter(hospital__id=hospital_id)
        return BestSurgeon.objects.all()

class BestTreatmentListView(generics.ListAPIView):
    serializer_class = BestTreatmentSerializer

    def get_queryset(self):
        hospital_id = self.kwargs.get('hospital_id')
        if hospital_id:
            return BestTreatment.objects.filter(hospital_id=hospital_id)
        return BestTreatment.objects.all()

