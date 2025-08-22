from rest_framework import serializers
from .models import Doctor, Education, Certification, SpecializationIcon,Specialization

class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = '__all__'

class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = '__all__'

class SpecializationIconSerializer(serializers.ModelSerializer):
    class Meta:
        model = SpecializationIcon
        fields = '__all__'

class SpecializationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialization
        fields = '__all__'

class DoctorSerializer(serializers.ModelSerializer):
    educations = EducationSerializer(many=True, read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)
    specialization = SpecializationIconSerializer(read_only=True)

    class Meta:
        model = Doctor
        fields = '__all__'
