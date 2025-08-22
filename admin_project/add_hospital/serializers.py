from rest_framework import serializers
from .models import HospitalGallery, HospitalAward
from datetime import date

class HospitalGallerySerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalGallery
        fields = '__all__'

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required.")
        if len(value) > 100:
            raise serializers.ValidationError("Title must be less than 100 characters.")
        return value

    def validate_category(self, value):
        if value and len(value) > 100:
            raise serializers.ValidationError("Category must be less than 100 characters.")
        return value

    def validate_uploaded_by(self, value):
        if value and len(value) > 100:
            raise serializers.ValidationError("Uploader name must be less than 100 characters.")
        return value

    def validate_image(self, value):
        valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
        ext = str(value.name).split('.')[-1].lower()
        if ext not in valid_extensions:
            raise serializers.ValidationError("Only jpg, jpeg, png, and webp images are allowed.")
        return value


class HospitalAwardSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalAward
        fields = '__all__'

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title is required.")
        if len(value) > 150:
            raise serializers.ValidationError("Title must be less than 150 characters.")
        return value

    def validate_awarded_by(self, value):
        if not value.strip():
            raise serializers.ValidationError("Awarded by is required.")
        if len(value) > 150:
            raise serializers.ValidationError("Awarded by must be less than 150 characters.")
        return value

    def validate_award_type(self, value):
        if value and len(value) > 100:
            raise serializers.ValidationError("Award type must be less than 100 characters.")
        return value

    def validate_location(self, value):
        if value and len(value) > 150:
            raise serializers.ValidationError("Location must be less than 150 characters.")
        return value

    def validate_award_date(self, value):
        if value > date.today():
            raise serializers.ValidationError("Award date cannot be in the future.")
        return value

    def validate_image(self, value):
        if value:
            valid_extensions = ['jpg', 'jpeg', 'png', 'webp']
            ext = str(value.name).split('.')[-1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError("Only jpg, jpeg, png, and webp images are allowed.")
        return value

    def validate_certificate_file(self, value):
        if value:
            valid_extensions = ['pdf', 'docx', 'jpg', 'jpeg', 'png']
            ext = str(value.name).split('.')[-1].lower()
            if ext not in valid_extensions:
                raise serializers.ValidationError("Only pdf, docx, jpg, jpeg, or png files are allowed.")
        return value
