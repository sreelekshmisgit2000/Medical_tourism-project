from django.urls import path
from .views import super_admin_login 
from client_app.views import GlobalSearchAPIView
from client_app.views import (
    CustomerSignupView,
    customer_login,
    VerifySignupOTPView,
    VerifyLoginOTPView,
    CustomTokenObtainPairView , # 🔄 import the JWT view
    SendPasswordResetOTPView,
    VerifyPasswordResetOTPView,
    ResetPasswordView,
    ResendPasswordResetOTPView
)
from rest_framework_simplejwt.views import TokenRefreshView  # optional refresh

urlpatterns = [
    path('signup/', CustomerSignupView.as_view(), name='customer-signup'),
    path('verify-signup-otp/', VerifySignupOTPView.as_view(), name='verify-signup-otp'),
    path('login/', customer_login, name='customer-login'),
    path('verify-login-otp/', VerifyLoginOTPView.as_view(), name='verify-login-otp'),
    path('forgot-password/send-otp/', SendPasswordResetOTPView.as_view(), name='send-password-reset-otp'),
    path('forgot-password/verify-otp/', VerifyPasswordResetOTPView.as_view(), name='verify-password-reset-otp'),
    path('forgot-password/reset/', ResetPasswordView.as_view(), name='reset-password'),
    path('forgot-password/resend-otp/', ResendPasswordResetOTPView.as_view(), name='resend-password-reset-otp'),
    path("admin/login/", super_admin_login, name="super_admin_login"),

    # 🔐 JWT token endpoint
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),

    # 🔁 Optional: token refresh endpoint
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('search/', GlobalSearchAPIView.as_view(), name='global-search'),
]
