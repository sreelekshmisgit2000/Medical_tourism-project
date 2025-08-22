from rest_framework import serializers
from .models import Treatment, TreatmentDetail, TreatmentIntro
from doctor_app.models import Doctor
from .models import TreatmentCategory
from doctor_app.serializers import DoctorSerializer
from hospital_app.serializers import HospitalSerializer

class TreatmentCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentCategory
        fields = ['id', 'name', 'slug', 'image']

class DoctorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['name', 'clinic_address']  # adjust based on your Doctor model

class TreatmentSerializer(serializers.ModelSerializer):
    doctors = DoctorSerializer(many=True, read_only=True)
    hospitals = HospitalSerializer(many=True, read_only=True)
    class Meta:
        model = Treatment
        fields =  '__all__'

class TreatmentDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentDetail
        fields = '__all__'

class TreatmentIntroSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentIntro
        fields = '__all__'


