from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from accounts.views import (
    CustomerSignupView,
    customer_login,
    VerifySignupOTPView,
    VerifyLoginOTPView,
    SendPasswordResetOTPView,
    VerifyPasswordResetOTPView,
    ResetPasswordView
)

urlpatterns = [
    path('signup/', CustomerSignupView.as_view(), name='customer-signup'),
    path('verify-signup-otp/', VerifySignupOTPView.as_view(), name='verify-signup-otp'),
    path('login/', customer_login, name='customer-login'),
    path('verify-login-otp/', VerifyLoginOTPView.as_view(), name='verify-login-otp'),
     path('forgot-password/send-otp/', SendPasswordResetOTPView.as_view(), name='send-password-reset-otp'),
    path('forgot-password/verify-otp/', VerifyPasswordResetOTPView.as_view(), name='verify-password-reset-otp'),
    path('forgot-password/reset/', ResetPasswordView.as_view(), name='reset-password'),



    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

]
