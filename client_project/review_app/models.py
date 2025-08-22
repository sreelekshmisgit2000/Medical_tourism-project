from django.db import models
from doctor_app.models import Doctor  # Import the Doctor model

class DoctorReview(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='doctor_reviews')
    reviewer_name = models.CharField(max_length=100)
    reviewer_picture = models.ImageField(upload_to='reviewer_pictures/', blank=True, null=True)
    review_text = models.TextField()
    rating = models.FloatField(default=0.0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for {self.doctor.name} by {self.reviewer_name}"

    class Meta:
        ordering = ['-created_at']
