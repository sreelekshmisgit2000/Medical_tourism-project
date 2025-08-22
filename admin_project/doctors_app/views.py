from rest_framework import viewsets
from .models import Doctor, Education, Certification, SpecializationIcon
from .serializers import DoctorSerializer, EducationSerializer, CertificationSerializer, SpecializationIconSerializer
from .models import Specialization
from .serializers import SpecializationSerializer
class DoctorViewSet(viewsets.ModelViewSet):

    
    queryset = Doctor.objects.all().order_by('-created_at')
    serializer_class = DoctorSerializer

class EducationViewSet(viewsets.ModelViewSet):
    queryset = Education.objects.all()
    serializer_class = EducationSerializer

class CertificationViewSet(viewsets.ModelViewSet):
    queryset = Certification.objects.all()
    serializer_class = CertificationSerializer



class SpecializationViewSet(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = SpecializationSerializer

class SpecializationIconViewSet(viewsets.ModelViewSet):
    queryset = SpecializationIcon.objects.all()
    serializer_class = SpecializationIconSerializer
