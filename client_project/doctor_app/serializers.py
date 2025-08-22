from rest_framework import serializers
from .models import Doctor, Education, Certification, SpecializationIcon
from review_app.models import DoctorReview
from hospital_app.models import Specialty
from django.db.models import Avg

class SpecializationIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecializationIcon
        fields = '__all__'

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'
        read_only_fields = ('id',)

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'
        read_only_fields = ('id',)


# Import SpecialtySerializer here to avoid circular import
from hospital_app.serializers import SpecialtySerializer

class DoctorSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, required=False)
    certifications = CertificationSerializer(many=True, required=False)
    profile_picture_url = serializers.SerializerMethodField()
    specialization = SpecialtySerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_profile_picture_url(self, obj):
        if obj.profile_picture and hasattr(obj.profile_picture, 'url'):
            return obj.profile_picture.url
        return None

    def to_internal_value(self, data):
        import json
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Convert specialization to int if it's a string
        if 'specialization' in data and isinstance(data['specialization'], str) and data['specialization'].isdigit():
            data['specialization'] = int(data['specialization'])

        # Handle educations and certifications if they are JSON strings
        if 'educations' in data and isinstance(data['educations'], str):
            try:
                data['educations'] = json.loads(data['educations'])
            except json.JSONDecodeError:
                # Handle case where string is not valid JSON
                data['educations'] = []
        
        if 'certifications' in data and isinstance(data['certifications'], str):
            try:
                data['certifications'] = json.loads(data['certifications'])
            except json.JSONDecodeError:
                data['certifications'] = []

        return super().to_internal_value(data)

    def create(self, validated_data):
        educations_data = validated_data.pop('educations', [])
        certifications_data = validated_data.pop('certifications', [])
        doctor = Doctor.objects.create(**validated_data)
        for edu in educations_data:
            Education.objects.create(doctor=doctor, **edu)
        for cert in certifications_data:
            Certification.objects.create(doctor=doctor, **cert)
        return doctor

    def update(self, instance, validated_data):
        educations_data = validated_data.pop('educations', None)
        certifications_data = validated_data.pop('certifications', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if educations_data is not None:
            instance.educations.all().delete()
            for edu in educations_data:
                Education.objects.create(doctor=instance, **edu)
        if certifications_data is not None:
            instance.certifications.all().delete()
            for cert in certifications_data:
                Certification.objects.create(doctor=instance, **cert)
        return instance


class DoctorReviewSerializer(serializers.ModelSerializer):
    doctor_details = serializers.SerializerMethodField()  # for response

    class Meta:
        model = DoctorReview
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'doctor_details')

    def get_doctor_details(self, obj):
        if obj.doctor:
            return {
                'id': obj.doctor.id,
                'name': obj.doctor.name
            }
        return None

