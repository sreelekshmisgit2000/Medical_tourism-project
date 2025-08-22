from rest_framework import serializers
from .models import Review

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

    def validate_client_name(self, value):
        if not value.strip():
            raise serializers.ValidationError("Client name is required.")
        return value

    def validate_review_text(self, value):
        if not value.strip():
            raise serializers.ValidationError("Review text is required.")
        return value

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
