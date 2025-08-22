from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from django_filters import rest_framework as filters

from .models import TimeSlot
from .serializers import TimeSlotSerializer, TimeSlotListSerializer


class TimeSlotFilter(filters.FilterSet):
    doctor = filters.NumberFilter(field_name='doctor_id')
    date = filters.DateFilter()
    date_from = filters.DateFilter(field_name='date', lookup_expr='gte')
    date_to = filters.DateFilter(field_name='date', lookup_expr='lte')
    status = filters.CharFilter()
    is_available = filters.BooleanFilter(method='filter_available')

    def filter_available(self, queryset, name, value):
        if value:
            return queryset.filter(status='available', is_active=True)
        return queryset

    class Meta:
        model = TimeSlot
        fields = ['doctor', 'date', 'status', 'is_active']


class TimeSlotViewSet(viewsets.ModelViewSet):
    queryset = TimeSlot.objects.all().order_by('date', 'start_time')
    serializer_class = TimeSlotSerializer
    filterset_class = TimeSlotFilter

    # ✅ Admin-only access
    permission_classes = [IsAdminUser]
    authentication_classes = [JWTAuthentication]

    def get_serializer_class(self):
        if self.action == 'list':
            return TimeSlotListSerializer
        return TimeSlotSerializer

    def get_queryset(self):
        queryset = super().get_queryset()

        doctor_id = self.request.query_params.get('doctor_id')
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)

        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        if date_from:
            queryset = queryset.filter(date__gte=date_from)
        if date_to:
            queryset = queryset.filter(date__lte=date_to)

        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        available_only = self.request.query_params.get('available_only')
        if available_only and available_only.lower() == 'true':
            queryset = queryset.filter(status='available', is_active=True)

        return queryset

    @action(detail=False, methods=['get'])
    def available_slots(self, request):
        queryset = self.get_queryset().filter(status='available', is_active=True)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def doctor_slots(self, request):
        doctor_id = request.query_params.get('doctor_id')
        if not doctor_id:
            return Response({'error': 'doctor_id parameter is required'}, status=status.HTTP_400_BAD_REQUEST)

        queryset = self.get_queryset().filter(doctor_id=doctor_id)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def book_slot(self, request, pk=None):
        time_slot = self.get_object()
        if time_slot.status != 'available':
            return Response({'error': 'Slot is not available for booking'}, status=status.HTTP_400_BAD_REQUEST)

        time_slot.status = 'booked'
        time_slot.save()
        serializer = self.get_serializer(time_slot)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def cancel_slot(self, request, pk=None):
        time_slot = self.get_object()
        if time_slot.status != 'booked':
            return Response({'error': 'Slot is not booked'}, status=status.HTTP_400_BAD_REQUEST)

        time_slot.status = 'cancelled'
        time_slot.save()
        serializer = self.get_serializer(time_slot)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def complete_slot(self, request, pk=None):
        time_slot = self.get_object()
        if time_slot.status != 'booked':
            return Response({'error': 'Slot is not booked'}, status=status.HTTP_400_BAD_REQUEST)

        time_slot.status = 'completed'
        time_slot.save()
        serializer = self.get_serializer(time_slot)
        return Response(serializer.data)
