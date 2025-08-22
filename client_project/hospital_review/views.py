from rest_framework import generics
from .models import HospitalReview
from .serializers import HospitalReviewSerializer
from .serializers import HospitalAverageRatingSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Avg

class HospitalReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = HospitalReviewSerializer

    def get_queryset(self):
        hospital_id = self.kwargs['hospital_id']
        return HospitalReview.objects.filter(hospital_id=hospital_id).order_by('-created_at')

    def perform_create(self, serializer):
        hospital_id = self.kwargs['hospital_id']
        serializer.save(hospital_id=hospital_id)

class HospitalAverageRatingView(APIView):
    def get(self, request, hospital_id):
        average = HospitalReview.objects.filter(hospital_id=hospital_id, is_active=True).aggregate(avg_rating=Avg('rating'))
        avg_rating = average['avg_rating']

        if avg_rating is None:
            avg_rating = 0.0

        data = {'average_rating': round(avg_rating, 1)}
        serializer = HospitalAverageRatingSerializer(data)
        return Response(serializer.data, status=status.HTTP_200_OK)