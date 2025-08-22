# permission_app/models.py

from django.db import models
from django.contrib.auth import get_user_model
from webinar_app.models import Webinar


User = get_user_model()

class PermissionModelRegistry(models.Model):
    name = models.CharField(max_length=100)        # Display name
    app_label = models.CharField(max_length=100)   # App name
    model_name = models.CharField(max_length=100, unique=True)  # Model name

    def __str__(self):
        return self.model_name.capitalize()

class ModelPermission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    permission_model = models.ForeignKey(PermissionModelRegistry, on_delete=models.CASCADE)
    can_create = models.BooleanField(default=False)
    can_read = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'permission_model')

    def __str__(self):
        return f"{self.user.username} - {self.permission_model.name}"
