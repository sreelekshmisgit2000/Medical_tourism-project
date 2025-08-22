from django.urls import path
from . import views

urlpatterns = [
   
    path('gallery/', views.HospitalGalleryListCreateView.as_view(), name='gallery-list-create'),
    path('gallery/<int:pk>/', views.HospitalGalleryRetrieveUpdateDestroyView.as_view(), name='gallery-detail'),

   
    path('awards/', views.HospitalAwardListCreateView.as_view(), name='award-list-create'),
    path('awards/<int:pk>/', views.HospitalAwardRetrieveUpdateDestroyView.as_view(), name='award-detail'),
]
