from rest_framework import serializers
from .models import (
    Treatment, TreatmentCategory, AlliedService, Accreditation,
    TreatmentSchedule, TreatmentEquipment, ServiceSchedule, AccreditationRenewal
)
from datetime import date


class TreatmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentCategory
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_name(self, value):
        if TreatmentCategory.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Category with this name already exists.")
        return value


class TreatmentEquipmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentEquipment
        fields = '__all__'

    def validate_quantity_needed(self, value):
        if value < 1:
            raise serializers.ValidationError("Quantity must be at least 1.")
        return value


class TreatmentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentSchedule
        fields = '__all__'

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data


class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_name(self, value):
        if Treatment.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("Treatment with this name already exists.")
        return value

    def validate_cost(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError("Cost cannot be negative.")
        return value

    def validate_success_rate(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError("Success rate must be between 0 and 100.")
        return value


class AlliedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlliedService
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_cost(self, value):
        if value < 0:
            raise serializers.ValidationError("Cost must be greater than or equal to 0.")
        return value

    def validate_duration_minutes(self, value):
        if value is not None and value <= 0:
            raise serializers.ValidationError("Duration must be greater than 0 minutes.")
        return value


class AccreditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accreditation
        fields = '__all__'
        read_only_fields = ('created_at', 'updated_at')

    def validate_valid_to(self, value):
        if value < date.today():
            raise serializers.ValidationError("Valid to date cannot be in the past.")
        return value

    def validate(self, data):
        if 'valid_from' in data and 'valid_to' in data:
            if data['valid_from'] >= data['valid_to']:
                raise serializers.ValidationError("Valid from date must be before valid to date.")
        return data


class ServiceScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceSchedule
        fields = '__all__'

    def validate(self, data):
        if data['start_time'] >= data['end_time']:
            raise serializers.ValidationError("Start time must be before end time.")
        return data


class AccreditationRenewalSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccreditationRenewal
        fields = '__all__'