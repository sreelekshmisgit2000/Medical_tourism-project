from rest_framework import serializers
from .models import Hospital, HospitalGallery, Specialty,Accreditation, AlliedService, HospitalAward, HospitalType,generate_unique_slug
from .models import BestSurgeon, BestTreatment
from doctor_app.models import Doctor
from treatment_app.models import Treatment
from hospital_review.serializers import HospitalReviewSerializer

class HospitalGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalGallery
        fields = '__all__'
        read_only_fields = ('id', 'uploaded_at')

class HospitalAwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalAward
        fields = '__all__'
        read_only_fields = ('id', 'created_at')

class HospitalSerializer(serializers.ModelSerializer):
    logo_url = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()
    galleries = HospitalGallerySerializer(many=True, required=False)
    awards = HospitalAwardSerializer(many=True, required=False)
    hospital_reviews = HospitalReviewSerializer(many=True, read_only=True)

    class Meta:
        model = Hospital
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')

    def get_logo_url(self, obj):
        if obj.logo and hasattr(obj.logo, 'url'):
            return obj.logo.url
        return None

    def get_cover_image_url(self, obj):
        if obj.cover_image and hasattr(obj.cover_image, 'url'):
            return obj.cover_image.url
        return None

    def validate(self, data):
        """
        Custom validation for hospital data
        """
        # Only check required fields for creation, not for partial updates
        if self.instance is None:  # Creating new hospital
            required_fields = ['name', 'address', 'city', 'country', 'phone', 'email']
            for field in required_fields:
                if field not in data or not data[field]:
                    raise serializers.ValidationError({field: f"{field} is required"})

        # Ensure slug is unique if provided
        slug = data.get('slug')
        name = data.get('name')
        if not slug or slug.strip() == '':
            # Generate a unique slug from name
            if name:
                data['slug'] = generate_unique_slug(name)
        else:
            # If slug exists, ensure it's unique
            if Hospital.objects.filter(slug=slug).exclude(pk=getattr(self.instance, 'pk', None)).exists():
                raise serializers.ValidationError({'slug': 'A hospital with this slug already exists. Please choose a different slug.'})
        return data

    def create(self, validated_data):
        galleries_data = validated_data.pop('galleries', [])
        awards_data = validated_data.pop('awards', [])
        hospital = Hospital.objects.create(**validated_data)
        for gallery in galleries_data:
            HospitalGallery.objects.create(hospital=hospital, **gallery)
        for award in awards_data:
            HospitalAward.objects.create(hospital=hospital, **award)
        return hospital

    def update(self, instance, validated_data):
        galleries_data = validated_data.pop('galleries', None)
        awards_data = validated_data.pop('awards', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if galleries_data is not None:
            instance.galleries.all().delete()
            for gallery in galleries_data:
                HospitalGallery.objects.create(hospital=instance, **gallery)
        if awards_data is not None:
            instance.awards.all().delete()
            for award in awards_data:
                HospitalAward.objects.create(hospital=instance, **award)
        return instance

    def to_internal_value(self, data):
        import json
        # Make a mutable copy of data (works for both QueryDict and dict)
        data = data.copy() if hasattr(data, 'copy') else dict(data)

        # Convert booleans sent as strings
        for field in ['is_active', 'parking_available', 'pharmacy_available', 'blood_bank_available',
                      'icu_beds_available', 'suite_rooms_available', 'vip_rooms_available']:
            if field in data:
                val = data.get(field)
                if isinstance(val, str):
                    if val.lower() == 'true':
                        data[field] = True
                    elif val.lower() == 'false':
                        data[field] = False

        # Parse JSON arrays sent as strings for multi-select fields
        for field in ['specialties', 'treatments', 'allied_services']:
            if field in data:
                val = data.get(field)
                if isinstance(val, str):
                    try:
                        data[field] = json.loads(val)
                    except Exception:
                        data[field] = []

        # Handle accreditation as a single ID (ForeignKey)
        if 'accreditation' in data:
            val = data.get('accreditation')
            if val == '' or val is None:
                data['accreditation'] = None  # Allow null since field is optional
            elif isinstance(val, str):
                try:
                    # Ensure it's a valid integer ID
                    data['accreditation'] = int(val)
                except (ValueError, TypeError):
                    data['accreditation'] = None  # Invalid ID, set to None
            else:
                data['accreditation'] = val  # Already an integer, pass through

        return super().to_internal_value(data)

class SpecialtySerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = Specialty
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None
    
class HospitalTypeSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = HospitalType
        fields = '__all__'
        read_only_fields = ('id', 'created_at', 'updated_at')
    def get_image_url(self, obj):
        if obj.image and hasattr(obj.image, 'url'):
            return obj.image.url
        return None

class AlliedServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlliedService
        fields = '__all__'

class AccreditationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Accreditation
        fields = '__all__' 

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'

class HospitalMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = ['id', 'name', 'city', 'logo']

class DoctorMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = ['id', 'name', 'specialization', 'profile_picture', 'is_active'] 

class BestSurgeonSerializer(serializers.ModelSerializer):
    hospital = HospitalMiniSerializer(read_only=True)
    doctor = DoctorMiniSerializer(read_only=True)

    class Meta:
        model = BestSurgeon
        fields = ['id', 'hospital', 'doctor']

class BestTreatmentSerializer(serializers.ModelSerializer):
    treatment_title = serializers.CharField(source='treatment.title', read_only=True)
    treatment_image = serializers.ImageField(source='treatment.image', read_only=True)

    class Meta:
        model = BestTreatment
        fields = ['id', 'treatment', 'treatment_title', 'treatment_image']