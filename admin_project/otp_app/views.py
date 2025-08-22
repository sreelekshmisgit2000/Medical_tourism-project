from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import OTP
from .serializers import SendOTPSerializer, VerifyOTPSerializer, ResetPasswordSerializer
import random

User = get_user_model()
from django.core.mail import send_mail, BadHeaderError



class SendOTPView(APIView):
    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"status": "fail", "message": "Email not registered"}, status=404)

           
            OTP.objects.filter(user=user).delete()

            otp_code = str(random.randint(10000, 99999))
            OTP.objects.create(user=user, code=otp_code)

            try:
                send_mail(
                    subject="Your OTP Code",
                    message=f"Your OTP is: {otp_code}",
                    from_email='sreelekshmisgit@gmail.com',
                    recipient_list=[email],
                    fail_silently=False,
                )
                print(" OTP sent to:", email)
            except BadHeaderError:
                print(" Invalid header found.")
                return Response({"status": "fail", "message": "Invalid email header."}, status=400)
            except Exception as e:
                print(" Email sending failed:", str(e))
                return Response({"status": "fail", "message": "OTP sending failed"}, status=500)

            return Response({"status": "success", "message": "OTP sent successfully"}, status=200)
        
        return Response(serializer.errors, status=400)


class VerifyOTPView(APIView):
    def post(self, request):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']
            try:
                user = User.objects.get(email=email)
                otp_obj = OTP.objects.filter(user=user, code=otp).first()

                if otp_obj:
                    if otp_obj.is_expired():
                        return Response({"status": "fail", "message": "OTP expired"}, status=400)
                    else:
                       
                        otp_obj.delete()
                        return Response({"status": "success", "message": "OTP verified"}, status=200)
                else:
                    return Response({"status": "fail", "message": "Invalid OTP"}, status=400)
            except User.DoesNotExist:
                return Response({"status": "fail", "message": "Invalid email"}, status=404)
        return Response(serializer.errors, status=400)


class ResetPasswordView(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
                user.set_password(new_password)
                user.save()
                return Response({"status": "success", "message": "Password reset successful"}, status=200)
            except User.DoesNotExist:
                return Response({"status": "fail", "message": "Invalid email"}, status=404)
        return Response(serializer.errors, status=400)
