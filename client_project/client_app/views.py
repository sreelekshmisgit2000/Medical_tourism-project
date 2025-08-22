# views.py

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.mail import send_mail
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from datetime import timedelta
import json
import random
from .serializers import SendPasswordResetOTPSerializer, VerifyPasswordResetOTPSerializer, ResetPasswordSerializer
from .models import PasswordResetOTP
from django.conf import settings
from django.contrib.auth import get_user_model
from client_app.serializers import CustomerSignupSerializer, CustomTokenObtainPairSerializer
from client_app.models import CustomUser
from otp_app.models import OTP
from rest_framework_simplejwt.views import TokenObtainPairView
from hospital_app.models import Hospital
from doctor_app.models import Doctor
from treatment_app.models import Treatment

User = get_user_model()

@csrf_exempt
def super_admin_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            print("Received data:", data)
            email = data.get("email")
            password = data.get("password")
            print(f"Trying to authenticate admin: {email}")

            if not email or not password:
                return JsonResponse({"status": "fail", "message": "Email and password are required"}, status=400)

            user = authenticate(request, username=email, password=password)
            print("User found:", user)

            if user is not None and user.is_staff:
                refresh = RefreshToken.for_user(user)
                return JsonResponse({
                    "status": "success",
                    "access": str(refresh.access_token),
                    "refresh": str(refresh),
                    "is_admin": True,  # ✅ Add this line
                    "user": {
                        "email": user.email,
                        "name": user.first_name or user.username,
                    }
                })
            else:
                return JsonResponse({"status": "fail", "message": "Invalid super admin credentials"}, status=401)

        except Exception as e:
            return JsonResponse({"status": "fail", "message": str(e)}, status=400)
    else:
        return JsonResponse({"status": "fail", "message": "Only POST allowed"}, status=405)


User = get_user_model()

def generate_otp():
    return str(random.randint(10000, 99999))




@csrf_exempt
def reset_admin_password(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        otp = data.get('otp')
        new_password = data.get('new_password')

        otp_obj = PasswordResetOTP.objects.filter(email=email, otp=otp, is_verified=True).last()
        if not otp_obj:
            return JsonResponse({'status': 'fail', 'message': 'OTP not verified'}, status=400)

        user = User.objects.filter(email=email, is_superuser=True).first()
        if not user:
            return JsonResponse({'status': 'fail', 'message': 'Admin not found'}, status=404)

        user.set_password(new_password)
        user.save()

        return JsonResponse({'status': 'success', 'message': 'Password reset successful'})



class CustomerSignupView(APIView):
    def post(self, request):
        serializer = CustomerSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            OTP.objects.filter(user=user).delete()

            otp_code = str(random.randint(10000, 99999))
            OTP.objects.create(user=user, code=otp_code)

            try:
                send_mail(
                    subject='Signup OTP',
                    message=f'Hi {user.first_name}, your OTP is: {otp_code}',
                    from_email='sreelekshmisgit@gmail.com',
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                print(" OTP sent to:", user.email)
            except Exception as e:
                print("Email sending failed:", str(e))
                return Response({"message": "Signup successful, but email failed to send."}, status=500)

            return Response({"message": "Customer registered successfully. OTP sent to email."}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifySignupOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = CustomUser.objects.get(email=email)
            latest_otp = OTP.objects.filter(user=user).order_by("-created_at").first()

            if latest_otp:
                if timezone.now() > latest_otp.created_at + timezone.timedelta(minutes=1):
                    return Response({"status": "fail", "message": "OTP expired"}, status=400)

                if latest_otp.code == otp:
                    user.is_verified = True
                    user.save()
                    return Response({"status": "success", "message": "Signup OTP verified"}, status=200)

            return Response({"status": "fail", "message": "Invalid OTP"}, status=400)
        except CustomUser.DoesNotExist:
            return Response({"status": "fail", "message": "User not found"}, status=404)


@csrf_exempt
def customer_login(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return JsonResponse({"status": "fail", "message": "Email and password are required"}, status=400)

        user = authenticate(request, username=email, password=password)

        if user is not None and not user.is_staff:
            OTP.objects.filter(user=user).delete()

            otp_code = str(random.randint(10000, 99999))
            OTP.objects.create(user=user, code=otp_code)

            send_mail(
                subject='Login OTP',
                message=f'Hi {user.first_name}, your OTP is: {otp_code}',
                from_email='sreelekshmisgit@gmail.com',
                recipient_list=[user.email],
                fail_silently=False,
            )

            return JsonResponse({
                "status": "success",
                "message": "OTP sent to email. Please verify.",
                "email": email
            }, status=200)
        else:
            return JsonResponse({"status": "fail", "message": "Invalid credentials or not a customer"}, status=401)

    return JsonResponse({"status": "error", "message": "Only POST method allowed"}, status=405)


class VerifyLoginOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")
        otp = request.data.get("otp")

        try:
            user = CustomUser.objects.get(email=email)
            latest_otp = OTP.objects.filter(user=user).order_by("-created_at").first()

            if latest_otp:
                if timezone.now() > latest_otp.created_at + timezone.timedelta(minutes=1):
                    return Response({"status": "fail", "message": "OTP expired"}, status=400)

                if latest_otp.code == otp:
                    refresh = RefreshToken.for_user(user)
                    return Response({
                        "status": "success",
                        "message": "Login successful",
                        "access": str(refresh.access_token),
                        "refresh": str(refresh),
                        "user": {
                            "email": user.email,
                            "name": user.first_name,
                            "is_verified": user.is_verified
                        }
                    }, status=200)

            return Response({"status": "fail", "message": "Invalid OTP"}, status=400)
        except CustomUser.DoesNotExist:
            return Response({"status": "fail", "message": "User not found"}, status=404)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class SendPasswordResetOTPView(APIView):
    def post(self, request):
        serializer = SendPasswordResetOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = CustomUser.objects.get(email=email)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

            otp = str(random.randint(10000, 99999))

            otp_obj, created = PasswordResetOTP.objects.update_or_create(
                email=email,
                defaults={
                    'otp': otp,
                    'is_verified': False,
                }
            )

            # ⚠️ Manually update created_at to now
            otp_obj.created_at = timezone.now()
            otp_obj.save()

            send_mail(
                subject='Password Reset OTP',
                message=f'Your OTP for password reset is: {otp}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
            )

            return Response({'status': 'success', 'message': 'OTP sent to email. Please verify.', 'email': email}, status=200)

        return Response(serializer.errors, status=400)


class VerifyPasswordResetOTPView(APIView):
    def post(self, request):
        serializer = VerifyPasswordResetOTPSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            otp = serializer.validated_data['otp']

            # 🔍 Instead of filtering by otp directly, get the latest one
            try:
                otp_obj = PasswordResetOTP.objects.filter(email=email).order_by('-created_at').first()

                # ✅ Debug log
                print(f"[DEBUG] Expected OTP: {otp_obj.otp}, Received: {otp}")

                if not otp_obj or otp_obj.otp != otp:
                    return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

                if otp_obj.is_verified:
                    return Response({'error': 'OTP already used'}, status=status.HTTP_400_BAD_REQUEST)

                if otp_obj.is_expired():
                    return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

                otp_obj.is_verified = True
                otp_obj.save()
                return Response({'message': 'OTP verified'}, status=status.HTTP_200_OK)

            except Exception:
                return Response({'error': 'Something went wrong'}, status=status.HTTP_400_BAD_REQUEST)
            
        else:
            print("[DEBUG] Serializer errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    

        


class ResetPasswordView(APIView):
    def post(self, request):
        email = request.data.get("email")
        new_password = request.data.get("new_password")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=404)
        
        # Ensure OTP was verified
        otp_obj = PasswordResetOTP.objects.filter(email=email, is_verified=True).order_by('-created_at').first()
        if not otp_obj:
            return Response({"error": "OTP not verified or expired."}, status=400)

        user.set_password(new_password)
        user.save()

        return Response({"message": "Password reset successful."})
    
class ResendPasswordResetOTPView(APIView):
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response({"error": "Email is required"}, status=400)

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'Email not found.'}, status=status.HTTP_404_NOT_FOUND)

        otp = str(random.randint(10000, 99999))

        otp_obj, created = PasswordResetOTP.objects.update_or_create(
            email=email,
            defaults={
                'otp': otp,
                'is_verified': False,
            }
        )

        otp_obj.created_at = timezone.now()
        otp_obj.save()

        send_mail(
            subject='Password Reset OTP (Resend)',
            message=f'Your OTP for password reset is: {otp}',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )

        return Response({'message': 'OTP resent successfully.'}, status=200)

class GlobalSearchAPIView(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('q', '').strip().lower()
        results = []

        if query:
            # Hospitals
            hospitals = Hospital.objects.filter(name__icontains=query)
            for hospital in hospitals:
                if hospital.slug:
                    results.append({
                        'id': hospital.id,
                        'name': hospital.name,
                        'type': 'hospital',
                        'slug': hospital.slug,
                        'path': f"/hospital/{hospital.slug}/",
                    })

            # Doctors
            doctors = Doctor.objects.filter(name__icontains=query)
            for doctor in doctors:
                if doctor.slug:
                    results.append({
                        'id': doctor.id,
                        'name': doctor.name,
                        'type': 'doctor',
                        'slug': doctor.slug,
                        'path': f"/doctor/{doctor.slug}/",
                    })

            # Treatments
            treatments = Treatment.objects.filter(title__icontains=query)
            for treatment in treatments:
                if treatment.slug:
                    results.append({
                        'id': treatment.id,
                        'name': treatment.title,
                        'type': 'treatment',
                        'slug': treatment.slug,
                        'path': f"/treatments/{treatment.slug}/",
                    })

        return Response(results, status=status.HTTP_200_OK)