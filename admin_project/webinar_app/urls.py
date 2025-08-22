from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WebinarViewSet, WebinarBookingViewSet

router = DefaultRouter()
router.register('webinars', WebinarViewSet)
router.register('bookings', WebinarBookingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
