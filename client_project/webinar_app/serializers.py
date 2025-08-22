from rest_framework import serializers
from .models import Webinar,WebinarBooking
from django.utils import timezone



class WebinarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Webinar
        fields = '__all__'

    # 🔹 Validate: Date must be future or today
    def validate_date(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Webinar date must be in the future.")
        return value

    # 🔹 Validate: Registration deadline must be before the date
    def validate_registration_deadline(self, value):
        date = self.initial_data.get('date')
        if value and date and value >= timezone.datetime.fromisoformat(date):
            raise serializers.ValidationError("Registration deadline must be before webinar date.")
        return value

    # 🔹 Price validation
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return value



class WebinarBookingSerializer(serializers.ModelSerializer):
    webinar = serializers.SerializerMethodField()
    user = serializers.SerializerMethodField()
    status = serializers.SerializerMethodField()  # <- Add this

    def get_webinar(self, obj):
        return obj.webinar.treatment.title

    def get_user(self, obj):
        return obj.user.email

    def get_status(self, obj):
        return "Attended" if obj.attended else "Booked"

    class Meta:
        model = WebinarBooking
        fields = [
            'id',
            'user',
            'webinar',
            'razorpay_order_id',
            'razorpay_payment_id',
            'razorpay_signature',
            'is_paid',
            'created_at',
            'status',     # <- Expose human-readable status
            'attended',   # <- Needed to allow updates from admin
        ]
        read_only_fields = [
            'razorpay_payment_id',
            'razorpay_signature',
            'is_paid',
            'created_at',
            'status',  # only read visible string
        ]

