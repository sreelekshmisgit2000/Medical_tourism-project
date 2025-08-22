from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DoctorViewSet, EducationViewSet, CertificationViewSet, SpecializationIconViewSet

router = DefaultRouter()
router.register(r'doctors', DoctorViewSet)
router.register(r'educations', EducationViewSet)
router.register(r'certifications', CertificationViewSet)
router.register(r'specializations', SpecializationIconViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]
