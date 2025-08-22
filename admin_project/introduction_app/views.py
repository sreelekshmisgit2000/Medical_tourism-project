from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import *
from .serializers import *

class IntroductionViewSet(viewsets.ModelViewSet):
    queryset = Introduction.objects.filter(is_active=True)
    serializer_class = IntroductionSerializer
    permission_classes = [IsAdminUser]

class SymptomsViewSet(viewsets.ModelViewSet):
    queryset = Symptoms.objects.filter(is_active=True)
    serializer_class = SymptomsSerializer
    permission_classes = [IsAdminUser]

class RiskFactorsViewSet(viewsets.ModelViewSet):
    queryset = RiskFactors.objects.filter(is_active=True)
    serializer_class = RiskFactorsSerializer
    permission_classes = [IsAdminUser]

class PreparationOfSurgeryViewSet(viewsets.ModelViewSet):
    queryset = PreparationOfSurgery.objects.filter(is_active=True)
    serializer_class = PreparationOfSurgerySerializer
    permission_classes = [IsAdminUser]

class ProcedureViewSet(viewsets.ModelViewSet):
    queryset = Procedure.objects.filter(is_active=True)
    serializer_class = ProcedureSerializer
    permission_classes = [IsAdminUser]

class PostProcedureViewSet(viewsets.ModelViewSet):
    queryset = PostProcedure.objects.filter(is_active=True)
    serializer_class = PostProcedureSerializer
    permission_classes = [IsAdminUser]

class SuccessRateViewSet(viewsets.ModelViewSet):
    queryset = SuccessRate.objects.filter(is_active=True)
    serializer_class = SuccessRateSerializer
    permission_classes = [IsAdminUser]

class FAQsViewSet(viewsets.ModelViewSet):
    queryset = FAQs.objects.filter(is_active=True).order_by('order')
    serializer_class = FAQsSerializer
    permission_classes = [IsAdminUser]

class TopDoctorsViewSet(viewsets.ModelViewSet):
    queryset = TopDoctors.objects.filter(is_active=True)
    serializer_class = TopDoctorsSerializer
    permission_classes = [IsAdminUser]

class TopHospitalsViewSet(viewsets.ModelViewSet):
    queryset = TopHospitals.objects.filter(is_active=True)
    serializer_class = TopHospitalsSerializer
    permission_classes = [IsAdminUser]
