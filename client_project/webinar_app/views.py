from rest_framework import generics
from .models import Webinar, WebinarBooking, Payment
from .serializers import WebinarSerializer
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import razorpay
import json
from treatment_app.models import Treatment
from django.utils import timezone
import traceback
from datetime import timedelta

User = get_user_model()

class WebinarListView(generics.ListAPIView):
    queryset = Webinar.objects.filter(is_active=True).order_by('-date')
    serializer_class = WebinarSerializer

class WebinarDetailView(generics.RetrieveAPIView):
    queryset = Webinar.objects.filter(is_active=True)
    serializer_class = WebinarSerializer
    lookup_field = 'slug'

class WebinarForTreatmentView(APIView):
    def get(self, request, treatment_id):
        try:
            print(f"[DEBUG] treatment_id received: {treatment_id}")

            # Try fetching treatment
            treatment = get_object_or_404(Treatment, pk=treatment_id)
            print(f"[DEBUG] Found treatment: {treatment.title}")

            # Fetch existing webinar only
            webinar = Webinar.objects.get(treatment=treatment, is_active=True)
            print(f"[DEBUG] Found existing webinar: {webinar.title}")

            serializer = WebinarSerializer(webinar)
            return Response(serializer.data)

        except Webinar.DoesNotExist:
            return Response({"error": "Webinar not found for this treatment."}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            print("[ERROR]", str(e))
            traceback.print_exc()
            return Response(
                {"error": str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )

class CreateRazorpayOrder(APIView):
    def post(self, request):
        amount = request.data.get('amount')

        if not amount:
            return Response({'error': 'Amount is required'}, status=400)

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        data = {
            "amount": int(amount),
            "currency": "INR",
            "payment_capture": 1
        }

        payment = client.order.create(data=data)

        return Response({
            "order_id": payment["id"],
            "amount": payment["amount"],
            "currency": payment["currency"],
            "key": settings.RAZORPAY_KEY_ID
        })

class RazorpayPaymentSuccessView(APIView):
    def post(self, request):
        data = request.data

        razorpay_payment_id = data.get('razorpay_payment_id')
        razorpay_order_id = data.get('razorpay_order_id')
        razorpay_signature = data.get('razorpay_signature')
        amount = data.get('amount')
        treatment_id = data.get('treatment_id')
        user_email = data.get('user_id')

        if not all([razorpay_payment_id, razorpay_order_id, razorpay_signature, amount, treatment_id]):
            return Response({'error': 'Incomplete data'}, status=400)

        # Razorpay signature verification
        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature,
            })
        except razorpay.errors.SignatureVerificationError:
            return Response({'error': 'Invalid signature'}, status=400)

        # Fetch user and treatment
        user = User.objects.filter(email=user_email).first()
        treatment = Treatment.objects.filter(id=treatment_id).first()

        if not user or not treatment:
            return Response({'error': 'Invalid user or treatment'}, status=404)

        # ✅ Create a new webinar dynamically
        webinar = Webinar.objects.create(
            treatment=treatment,
            title=treatment.title,
            date=timezone.now() + timedelta(days=2),  # Placeholder date (optional)
            price=int(amount),  # Convert back to INR
            link="https://example.com/webinar/{}".format(treatment.slug),
            is_active=True
        )

        # ✅ Create a Payment record
        payment = Payment.objects.create(
            user=user,
            treatment=treatment,
            order_id=razorpay_order_id,
            payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            amount=int(amount),
            currency='INR',
            status='paid'
        )

        # ✅ Create WebinarBooking
        WebinarBooking.objects.create(
            user=user,
            webinar=webinar,
            razorpay_order_id=razorpay_order_id,
            razorpay_payment_id=razorpay_payment_id,
            razorpay_signature=razorpay_signature,
            is_paid=True
        )

        # ✅ Send confirmation email
        send_mail(
            subject="Webinar Request Successful",
            message=f"Hi {user.first_name or user.username},\n\nYour webinar for the treatment \"{treatment.title}\" has been successfully scheduled.\n\nYou will receive details soon.\n\nThank you!",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
        )

        return Response({'message': 'Webinar booked successfully.', 'payment_id': payment.id})


from django.db.models import Q

class WebinarBookingStatusView(APIView):
    def get(self, request, treatment_id):
        user_email = request.query_params.get('user_email')
        if not user_email:
            return Response({'error': 'Missing user_email'}, status=400)

        user = User.objects.filter(email=user_email).first()
        treatment = Treatment.objects.filter(id=treatment_id).first()

        if not user or not treatment:
            return Response({'error': 'Invalid user or treatment'}, status=404)

        webinar = Webinar.objects.filter(treatment=treatment).order_by('-date').first()
        if not webinar:
            return Response({'booked': False})

        booking = WebinarBooking.objects.filter(user=user, webinar=webinar).order_by('-created_at').first()

        if booking:
            return Response({
                'booked': True,
                'attended': booking.attended  # ✨ add attended status
            })

        return Response({'booked': False})


class UserWebinarListView(APIView):
    def get(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({"error": "Email is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        
        bookings = WebinarBooking.objects.filter(user=user).select_related('webinar')
        webinars = [booking.webinar for booking in bookings]
        serializer = WebinarSerializer(webinars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)