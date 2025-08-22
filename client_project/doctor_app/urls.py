from django.urls import path
from .views import DoctorListCreateView, DoctorDetailView, AllDoctorsView

urlpatterns = [
    #  List & Create doctors
    path('doctorslist/', DoctorListCreateView.as_view(), name='doctor-list-create'),

    # Doctor detail by slug
    path('<slug:slug>/', DoctorDetailView.as_view(), name='doctor-detail'),

    #  Count + Full list of doctors (optional separate endpoint)
    path('api/doctors/total/', AllDoctorsView.as_view(), name='doctor-total-list'),
]
