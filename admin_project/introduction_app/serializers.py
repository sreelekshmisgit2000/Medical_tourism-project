from rest_framework import serializers
from .models import *

class IntroductionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Introduction
        fields = '__all__'

    def validate_title(self, value):
        if not value:
            raise serializers.ValidationError("Title is required.")
        return value

class SymptomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symptoms
        fields = '__all__'

    def validate_description(self, value):
        if not value:
            raise serializers.ValidationError("Description is required.")
        return value

class RiskFactorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = RiskFactors
        fields = '__all__'

    def validate_risk_detail(self, value):
        if len(value) < 10:
            raise serializers.ValidationError("Risk detail must be at least 10 characters.")
        return value

class PreparationOfSurgerySerializer(serializers.ModelSerializer):
    class Meta:
        model = PreparationOfSurgery
        fields = '__all__'

    def validate_preparation(self, value):
        if not value:
            raise serializers.ValidationError("Preparation info is required.")
        return value

class ProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedure
        fields = '__all__'

    def validate_steps(self, value):
        if not value:
            raise serializers.ValidationError("Procedure steps must be provided.")
        return value

class PostProcedureSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostProcedure
        fields = '__all__'

    def validate_care(self, value):
        if not value:
            raise serializers.ValidationError("Post-care details must be provided.")
        return value

class SuccessRateSerializer(serializers.ModelSerializer):
    class Meta:
        model = SuccessRate
        fields = '__all__'

    def validate_rate(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Rate must be between 0 and 100.")
        return value

class FAQsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQs
        fields = '__all__'

    def validate_question(self, value):
        if not value:
            raise serializers.ValidationError("Question is required.")
        return value

class TopDoctorsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopDoctors
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Doctor name is required.")
        return value

class TopHospitalsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TopHospitals
        fields = '__all__'

    def validate_name(self, value):
        if not value:
            raise serializers.ValidationError("Hospital name is required.")
        return value
