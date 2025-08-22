from django.db import models
from doctor_app.models import Doctor
from hospital_app.models import Hospital
from django.utils.text import slugify
from django_ckeditor_5.fields import CKEditor5Field

# 🔹 New Category Model
class TreatmentCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, default='active')

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Treatment(models.Model):
    TREATMENT_TYPE_CHOICES = [
        ('surgery', 'Surgery'),
        ('therapy', 'Therapy'),
        ('consultation', 'Consultation'),
        ('diagnostic', 'Diagnostic'),
        ('emergency', 'Emergency'),
        ('preventive', 'Preventive'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    title = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(TreatmentCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='treatments')
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPE_CHOICES, default='consultation')
    description = models.TextField()
    image = models.ImageField(upload_to='treatment_images/', null=True, blank=True)
    
    # New fields
    duration_days = models.PositiveIntegerField(null=True, blank=True)
    duration_hours = models.PositiveIntegerField(null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    insurance_coverage = models.BooleanField(default=False)
    requires_anesthesia = models.BooleanField(default=False)
    requires_room = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    doctors = models.ManyToManyField('doctor_app.Doctor', related_name='treatments', blank=True)
    hospitals = models.ManyToManyField('hospital_app.Hospital', related_name='treatments', blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)

    symptoms = CKEditor5Field(blank=True, null=True)
    faqs = CKEditor5Field(blank=True, null=True)
    risk_factors = CKEditor5Field(blank=True, null=True)
    preparations = CKEditor5Field(blank=True, null=True)
    procedure = CKEditor5Field(blank=True, null=True)
    post_procedure = CKEditor5Field(blank=True, null=True)
    success_rate = CKEditor5Field(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class TreatmentDetail(models.Model):
    treatment = models.OneToOneField(Treatment, on_delete=models.CASCADE, related_name="details")
    header_image = models.ImageField(upload_to='treatment_headers/', blank=True, null=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"Details for {self.treatment.title}"


class TreatmentIntro(models.Model):
    treatment = models.OneToOneField(Treatment, on_delete=models.CASCADE, related_name="intro")
    introduction = models.TextField(blank=True)
    before_image = models.ImageField(upload_to='treatment_intro/', blank=True, null=True)
    after_image = models.ImageField(upload_to='treatment_intro/', blank=True, null=True)
    stay_info = models.CharField(max_length=255, blank=True, null=True)
    duration_info = models.CharField(max_length=255, blank=True, null=True)
    anesthesia_info = models.CharField(max_length=255, blank=True, null=True)
    cost_info = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Intro for {self.treatment.title}"
