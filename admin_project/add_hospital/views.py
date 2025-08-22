from rest_framework import generics
from .models import HospitalGallery, HospitalAward
from .serializers import HospitalGallerySerializer, HospitalAwardSerializer

# --- HospitalGallery Views ---
class HospitalGalleryListCreateView(generics.ListCreateAPIView):
    queryset = HospitalGallery.objects.all().order_by('-uploaded_at')
    serializer_class = HospitalGallerySerializer

class HospitalGalleryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HospitalGallery.objects.all()
    serializer_class = HospitalGallerySerializer


# --- HospitalAward Views ---
class HospitalAwardListCreateView(generics.ListCreateAPIView):
    queryset = HospitalAward.objects.all().order_by('-award_date')
    serializer_class = HospitalAwardSerializer

class HospitalAwardRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = HospitalAward.objects.all()
    serializer_class = HospitalAwardSerializer
