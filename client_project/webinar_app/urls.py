from django.urls import path
from .views import CreateRazorpayOrder, RazorpayPaymentSuccessView, WebinarListView, WebinarDetailView,WebinarForTreatmentView, WebinarBookingStatusView, UserWebinarListView

urlpatterns = [
    path('api/webinars/', WebinarListView.as_view(), name='webinar-list'),
    path('api/webinars/<slug:slug>/', WebinarDetailView.as_view(), name='webinar-detail'),
    path('webinar-for-treatment/<int:treatment_id>/', WebinarForTreatmentView.as_view(), name='webinar_for_treatment'),
    path('create-order/', CreateRazorpayOrder.as_view(), name='create-razorpay-order'),
    path('payment/success/',RazorpayPaymentSuccessView.as_view(), name='payment-success'),
    path('webinar-booking-status/<int:treatment_id>/', WebinarBookingStatusView.as_view()),
    path('user-webinars/', UserWebinarListView.as_view(), name='user-webinars'),


    
]
