from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from datetime import timedelta


class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.username

from django.utils import timezone
from datetime import timedelta

class PasswordResetOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=1)

    def __str__(self):
        return f"{self.email} - OTP: {self.otp}"
