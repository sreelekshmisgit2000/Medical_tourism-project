from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from django.utils import timezone

class Webinar(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    date = models.DateTimeField()
    speaker = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    link = models.URLField()
    image = models.ImageField(upload_to='webinars/', blank=True, null=True)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    capacity = models.PositiveIntegerField(blank=True, null=True)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    recording_url = models.URLField(blank=True, null=True)
    language = models.CharField(max_length=50, blank=True)
    tags = models.CharField(max_length=200, blank=True)  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        errors = {}
        if self.price is not None and self.price < 0:
            errors['price'] = 'Price must be non-negative.'
        if self.capacity is not None and self.capacity < 1:
            errors['capacity'] = 'Capacity must be at least 1.'
        if self.registration_deadline and self.date:
            if self.registration_deadline > self.date:
                errors['registration_deadline'] = 'Registration deadline must be before the webinar date.'
        if self.date and self.date < timezone.now():
            errors['date'] = 'Webinar date must be in the future.'
        if errors:
            raise ValidationError(errors)

    def __str__(self):
        return self.title
    

class WebinarBooking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    webinar = models.ForeignKey('Webinar', on_delete=models.CASCADE)
    razorpay_order_id = models.CharField(max_length=100, unique=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=100, blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.webinar and self.webinar.capacity is not None:
            booked_count = WebinarBooking.objects.filter(webinar=self.webinar).count()
            if booked_count >= self.webinar.capacity:
                raise ValidationError('Webinar capacity has been reached.')

    def __str__(self):
        return f"{self.user} - {self.webinar.title}"
