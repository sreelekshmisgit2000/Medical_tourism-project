from rest_framework import generics
from .models import Doctor
from .serializers import DoctorSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

# ✅ Total doctors with count
class AllDoctorsView(APIView):
    def get(self, request):
        doctors = Doctor.objects.filter(is_active=True)
        serializer = DoctorSerializer(doctors, many=True)
        count = doctors.count()
        return Response({
            'total_doctors': count,
            'data': serializer.data
        })

# ✅ List + Create doctors
class DoctorListCreateView(generics.ListCreateAPIView):
    serializer_class = DoctorSerializer

    def get_queryset(self):
        return Doctor.objects.filter(is_active=True).order_by('-rating')

    def get_serializer(self, *args, **kwargs):
        
        if isinstance(kwargs.get('data', {}), list):
            kwargs['many'] = True
        return super().get_serializer(*args, **kwargs)

# ✅ Get detail by slug
class DoctorDetailView(generics.RetrieveAPIView):
    queryset = Doctor.objects.filter(is_active=True)
    serializer_class = DoctorSerializer
    lookup_field = 'slug'
