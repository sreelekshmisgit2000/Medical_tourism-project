from rest_framework import serializers
from .models import TimeSlot
from doctors_app.serializers import DoctorSerializer

class TimeSlotSerializer(serializers.ModelSerializer):
    doctor = DoctorSerializer(read_only=True)
    doctor_id = serializers.IntegerField(write_only=True)
    duration_minutes = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = TimeSlot
        fields = [
            'id', 'doctor', 'doctor_id', 'date', 'start_time', 'end_time',
            'status', 'is_active', 'duration_minutes', 'is_available',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """
        Validate that end_time is after start_time and no overlapping slots
        """
        start_time = data.get('start_time')
        end_time = data.get('end_time')
        date = data.get('date')
        doctor_id = data.get('doctor_id')
        
        if start_time and end_time and start_time >= end_time:
            raise serializers.ValidationError("End time must be after start time")
        
        # Check for overlapping slots
        if date and doctor_id and start_time and end_time:
            overlapping_slots = TimeSlot.objects.filter(
                doctor_id=doctor_id,
                date=date,
                is_active=True
            ).exclude(id=self.instance.id if self.instance else None)
            
            for slot in overlapping_slots:
                if (start_time < slot.end_time and end_time > slot.start_time):
                    raise serializers.ValidationError(
                        f"Time slot overlaps with existing slot: {slot.start_time}-{slot.end_time}"
                    )
        
        return data

class TimeSlotListSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.name', read_only=True)
    doctor_specialization = serializers.CharField(source='doctor.specialization.name', read_only=True)
    duration_minutes = serializers.ReadOnlyField()
    is_available = serializers.ReadOnlyField()
    
    class Meta:
        model = TimeSlot
        fields = [
            'id', 'doctor_name', 'doctor_specialization', 'date', 'start_time', 
            'end_time', 'status', 'duration_minutes', 'is_available'
        ]
