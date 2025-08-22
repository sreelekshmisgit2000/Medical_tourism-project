from django.urls import path
from .views import HospitalReviewListCreateAPIView
from .views import HospitalAverageRatingView

urlpatterns = [
    path('hospital/<int:hospital_id>/reviews/', HospitalReviewListCreateAPIView.as_view(), name='hospital-review-list-create'),
    path('hospitals/<int:hospital_id>/average-rating/', HospitalAverageRatingView.as_view(), name='hospital-average-rating'),
]
