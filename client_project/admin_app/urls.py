from django.urls import path


from .views import (
    AdminWebinarBookingInvoiceView,
    AdminWebinarBookingListView,
    AdminWebinarBookingRetrieveUpdateDestroyView,
    AdminWebinarListCreateView,
    AdminWebinarRetrieveUpdateDestroyView,
    DoctorListCreateView,
    DoctorRetrieveUpdateDestroyView,
    DoctorReviewListCreateView,
    DoctorReviewRetrieveUpdateDestroyView,
    HospitalListCreateView,
    HospitalRetrieveUpdateDestroyView,
    SpecialtyListCreateView,
    SpecialtyRetrieveUpdateDestroyView,
    HospitalTypeListCreateView,
    HospitalTypeRetrieveUpdateDestroyView,
    AlliedServiceListCreateView,
    AlliedServiceRetrieveUpdateDestroyView,
    AccreditationListCreateView,
    AccreditationRetrieveUpdateDestroyView,
    HospitalReviewListCreateView,
    HospitalReviewRetrieveUpdateDestroyView,
    HospitalAverageRatingView,
    TreatmentCategoryListCreateView,
    TreatmentCategoryRetrieveUpdateDestroyView,
    TreatmentDetailRetrieveUpdateDestroyView,
    TreatmentIntroRetrieveUpdateDestroyView,
    TreatmentListCreateView,
    TreatmentRetrieveUpdateDestroyView,
    TreatmentsByCategoryView,
    
)
from rest_framework.routers import DefaultRouter
# from . import urls_webinar
from django.urls import include

urlpatterns = [
    # Hospital CRUD endpoints
    path('hospitals/', HospitalListCreateView.as_view(), name='hospital-list-create'),
    path('hospitals/<int:pk>/', HospitalRetrieveUpdateDestroyView.as_view(), name='hospital-detail'),

    # Specialty CRUD endpoints
    path('specialties/', SpecialtyListCreateView.as_view(), name='specialty-list-create'),
    path('specialties/<int:pk>/', SpecialtyRetrieveUpdateDestroyView.as_view(), name='specialty-detail'),

    # HospitalType CRUD endpoints
    path('hospital-types/', HospitalTypeListCreateView.as_view(), name='hospital-type-list-create'),
    path('hospital-types/<int:pk>/', HospitalTypeRetrieveUpdateDestroyView.as_view(), name='hospital-type-detail'),
    # Treatment CRUD endpoints
    

    path('allied-services/', AlliedServiceListCreateView.as_view(), name='alliedservice-list-create'),
    path('allied-services/<int:pk>/', AlliedServiceRetrieveUpdateDestroyView.as_view(), name='alliedservice-detail'),

    path('accreditations/', AccreditationListCreateView.as_view(), name='accreditation-list-create'),
    path('accreditations/<int:pk>/', AccreditationRetrieveUpdateDestroyView.as_view(), name='accreditation-detail'),

  

    # Hospital Review CRUD endpoints
    path('hospital-reviews/', HospitalReviewListCreateView.as_view(), name='hospital-review-list-create'),
    path('hospital-reviews/<int:hospital_id>/', HospitalReviewRetrieveUpdateDestroyView.as_view(), name='hospital-review-detail'),
    path('hospitals/average-rating/<int:hospital_id>', HospitalAverageRatingView.as_view(), name='hospital-average-rating'),

    # Doctor CRUD endpoints
    path('doctors/', DoctorListCreateView.as_view(), name='doctor-list-create'),
    path('doctors/<int:pk>/', DoctorRetrieveUpdateDestroyView.as_view(), name='doctor-detail'),

    path('doctor-reviews/', DoctorReviewListCreateView.as_view(), name='doctor-review-list-create'),
    path('doctor-reviews/<int:pk>/', DoctorReviewRetrieveUpdateDestroyView.as_view(), name='doctor-review-detail'),

    path('treatments/', TreatmentListCreateView.as_view(), name='treatment-list-create'),
    path('treatments/<int:pk>/', TreatmentRetrieveUpdateDestroyView.as_view(), name='treatment-detail'),

    path('treatment-categories/', TreatmentCategoryListCreateView.as_view(), name='treatmentcategory-list-create'),
    path('treatment-categories/<int:pk>/', TreatmentCategoryRetrieveUpdateDestroyView.as_view(), name='treatmentcategory-detail'),
    path('treatment-intro/<int:pk>/', TreatmentIntroRetrieveUpdateDestroyView.as_view(), name='admin-treatment-intro-detail'),
    path('treatment-detail/<int:pk>/', TreatmentDetailRetrieveUpdateDestroyView.as_view(), name='admin-treatment-detail-detail'),
    path('treatments/category/<str:category_slug>/', TreatmentsByCategoryView.as_view(), name='treatments-by-category'),

   path('webinars/', AdminWebinarListCreateView.as_view(), name='admin-webinar-list-create'),
    path('webinars/<int:pk>/', AdminWebinarRetrieveUpdateDestroyView.as_view(), name='admin-webinar-detail'),
    
    # ✅ List all webinar bookings
    path('webinar-bookings/', AdminWebinarBookingListView.as_view(), name='admin-webinar-bookings'),
    
    # ✅ Detail (retrieve, update, delete) for a single booking
    path('webinar-bookings/<int:pk>/', AdminWebinarBookingRetrieveUpdateDestroyView.as_view(), name='admin-webinar-booking-detail'),

    path('webinar-bookings/<int:pk>/invoice/',AdminWebinarBookingInvoiceView.as_view(),name='admin-webinar-booking-invoice'),

    
    
    # path('', include('api.urls_webinar')),
] 