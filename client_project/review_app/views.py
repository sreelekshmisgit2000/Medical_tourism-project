from rest_framework import generics
from .models import DoctorReview
from .serializers import ReviewSerializer

class DoctorReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        doctor_id = self.kwargs['doctor_id']
        return DoctorReview.objects.filter(doctor_id=doctor_id).order_by('-created_at')

    def perform_create(self, serializer):
        doctor_id = self.kwargs['doctor_id']
        serializer.save(doctor_id=doctor_id)
