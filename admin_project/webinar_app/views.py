from rest_framework import viewsets
from .models import Webinar, WebinarBooking
from .serializers import WebinarSerializer, WebinarBookingSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication


class WebinarViewSet(viewsets.ModelViewSet):
    queryset = Webinar.objects.all().order_by('-created_at')
    serializer_class = WebinarSerializer
    permission_classes = [IsAdminUser]  # ✅ Only admin can access
    authentication_classes = [JWTAuthentication]


class WebinarBookingViewSet(viewsets.ModelViewSet):
    queryset = WebinarBooking.objects.all().order_by('-created_at')
    serializer_class = WebinarBookingSerializer
    permission_classes = [IsAdminUser]  # ✅ Only admin can access
    authentication_classes = [JWTAuthentication]
