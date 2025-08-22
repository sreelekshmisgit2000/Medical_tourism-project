from rest_framework import serializers
from .models import Webinar, WebinarBooking
from django.utils import timezone

class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = '__all__'

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be non-negative.")
        return value

    def validate_capacity(self, value):
      if value is None:
        raise serializers.ValidationError("Capacity is required.")
      if value < 1:
        raise serializers.ValidationError("Capacity must be at least 1.")
      return value


    def validate(self, data):
        date = data.get('date')
        deadline = data.get('registration_deadline')

        if date and date < timezone.now():
            raise serializers.ValidationError({"date": "Webinar date must be in the future."})
        if date and deadline and deadline > date:
            raise serializers.ValidationError({"registration_deadline": "Deadline must be before the webinar date."})
        return data

class WebinarBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebinarBooking
        fields = '__all__'

    def validate(self, data):
        webinar = data.get('webinar')
        if webinar and webinar.capacity is not None:
            count = WebinarBooking.objects.filter(webinar=webinar).count()
            if count >= webinar.capacity:
                raise serializers.ValidationError("Webinar capacity has been reached.")
        return data
