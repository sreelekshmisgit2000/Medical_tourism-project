from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from client_app.models import CustomUser
from django.contrib.auth import get_user_model
import re
from client_app.models import PasswordResetOTP
from django.utils import timezone 

class CustomerSignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    is_verified = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password', 'is_verified']

    def validate_email(self, value):
        if " " in value:
            raise serializers.ValidationError("Email should not contain spaces.")
        if '@' not in value:
            raise serializers.ValidationError("Email must contain '@'.")
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", value):
            raise serializers.ValidationError("Password must include at least one uppercase letter.")
        if not re.search(r"[a-z]", value):
            raise serializers.ValidationError("Password must include at least one lowercase letter.")
        if not re.search(r"[0-9]", value):
            raise serializers.ValidationError("Password must include at least one number.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", value):
            raise serializers.ValidationError("Password must include at least one special character.")
        return value

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['email'],  
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            is_customer=True,
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


# ✅ Custom Token Serializer for JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom fields to the token
        token['email'] = user.email
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['is_customer'] = user.is_customer
        token['is_doctor'] = user.is_doctor
        token['is_hospital'] = user.is_hospital

        return token


User = get_user_model()

class SendPasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()

class VerifyPasswordResetOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField()

    def validate(self, data):
        email = data.get('email')
        otp = data.get('otp')

        # ✅ Fetch the latest OTP for the email
        otp_obj = PasswordResetOTP.objects.filter(email=email).order_by('-created_at').first()

        if not otp_obj or otp_obj.otp != otp:
            raise serializers.ValidationError("Invalid OTP.")

        # Debugging
        from django.utils import timezone
        print(f"[DEBUG] OTP object created_at: {otp_obj.created_at}")
        print(f"[DEBUG] Current time: {timezone.now()}")
        print(f"[DEBUG] OTP expired: {otp_obj.is_expired()}")

        if otp_obj.is_expired():
            raise serializers.ValidationError("OTP has expired.")

        return data





class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    new_password = serializers.CharField(min_length=5)