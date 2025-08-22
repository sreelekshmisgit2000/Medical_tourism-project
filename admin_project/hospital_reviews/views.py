from rest_framework import viewsets, permissions
from .models import Review
from .serializers import ReviewSerializer

class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]  # Admin only edit/delete
        return [permissions.AllowAny()]  # Others view/add

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Review.objects.all().order_by('-created_at')
        return Review.objects.filter(is_active=True).order_by('-created_at')
