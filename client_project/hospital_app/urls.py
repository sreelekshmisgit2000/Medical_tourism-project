from django.urls import path
from .views import HospitalListCreateView, HospitalRetrieveUpdateDestroyView
from .views import BestSurgeonListView, BestTreatmentListView

urlpatterns = [
    path('', HospitalListCreateView.as_view(), name='hospital-list-create'),
    path('<int:pk>/', HospitalRetrieveUpdateDestroyView.as_view(), name='hospital-detail'),
    path('<int:hospital_id>/best-surgeons/', BestSurgeonListView.as_view(), name='best-surgeons'),
    path('<int:hospital_id>/best-treatments/', BestTreatmentListView.as_view()),
]
