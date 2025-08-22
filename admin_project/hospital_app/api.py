from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'treatments', TreatmentViewSet)
router.register(r'treatment-categories', TreatmentCategoryViewSet)
router.register(r'allied-services', AlliedServiceViewSet)
router.register(r'accreditations', AccreditationViewSet)
router.register(r'treatment-schedules', TreatmentScheduleViewSet)
router.register(r'treatment-equipments', TreatmentEquipmentViewSet)
router.register(r'service-schedules', ServiceScheduleViewSet)
router.register(r'accreditation-renewals', AccreditationRenewalViewSet)