from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'introduction', IntroductionViewSet)
router.register(r'symptoms', SymptomsViewSet)
router.register(r'risk-factors', RiskFactorsViewSet)
router.register(r'preparation', PreparationOfSurgeryViewSet)
router.register(r'procedure', ProcedureViewSet)
router.register(r'post-procedure', PostProcedureViewSet)
router.register(r'success-rate', SuccessRateViewSet)
router.register(r'faqs', FAQsViewSet)
router.register(r'top-doctors', TopDoctorsViewSet)
router.register(r'top-hospitals', TopHospitalsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
