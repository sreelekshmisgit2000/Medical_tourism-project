from django.db import models
from django.conf import settings  
from django.utils import timezone

class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)

    
    def is_expired(self):
        return timezone.now() > self.created_at + timezone.timedelta(minutes=1)


    def __str__(self):
        return f"{self.user.email} - {self.code}"
