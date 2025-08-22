# hospital_app/treatment_urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    TreatmentViewSet, TreatmentCategoryViewSet, AlliedServiceViewSet,
    AccreditationViewSet, TreatmentScheduleViewSet, TreatmentEquipmentViewSet,
    ServiceScheduleViewSet, AccreditationRenewalViewSet
)

# Create router and register viewsets
router = DefaultRouter()
router.register(r'treatments', TreatmentViewSet)
router.register(r'treatment-categories', TreatmentCategoryViewSet)
router.register(r'allied-services', AlliedServiceViewSet)
router.register(r'accreditations', AccreditationViewSet)
router.register(r'treatment-schedules', TreatmentScheduleViewSet)
router.register(r'treatment-equipment', TreatmentEquipmentViewSet)
router.register(r'service-schedules', ServiceScheduleViewSet)
router.register(r'accreditation-renewals', AccreditationRenewalViewSet)

app_name = 'hospital_app'

urlpatterns = [
    # API endpoints
    path('api/', include(router.urls)),
    
    # Additional custom endpoints
    path('api/treatments/<int:pk>/equipment/', 
         TreatmentViewSet.as_view({'get': 'equipment'}), 
         name='treatment-equipment'),
    
    path('api/treatments/<int:pk>/schedules/', 
         TreatmentViewSet.as_view({'get': 'schedules'}), 
         name='treatment-schedules'),
    
    path('api/allied-services/<int:pk>/schedules/', 
         AlliedServiceViewSet.as_view({'get': 'schedules'}), 
         name='allied-service-schedules'),
    
    path('api/accreditations/<int:pk>/renewals/', 
         AccreditationViewSet.as_view({'get': 'renewals'}), 
         name='accreditation-renewals'),
]
