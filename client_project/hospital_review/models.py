from django.db import models
from hospital_app.models import Hospital  # assuming you have a Hospital model


class HospitalReview(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='hospital_reviews')
    patient_name = models.CharField(max_length=100)
    patient_picture = models.ImageField(upload_to='patient_pictures/', blank=True, null=True)
    review_text = models.TextField()
    rating = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.hospital.name} by {self.patient_name}"

    class Meta:
        ordering = ['-created_at']
