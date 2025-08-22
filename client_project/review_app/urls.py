from django.urls import path
from .views import DoctorReviewListCreateAPIView

urlpatterns = [
    path('doctor/<int:doctor_id>/reviews/', DoctorReviewListCreateAPIView.as_view(), name='doctor-review-list-create'),
]
