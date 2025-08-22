from django.db import models

class SpecializationIcon(models.Model):
    name = models.CharField(max_length=100)
    icon = models.ImageField(upload_to='specialization_icons/', blank=True, null=True)

    def __str__(self):
        return self.name


class Doctor(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    specialization = models.ForeignKey(SpecializationIcon, on_delete=models.SET_NULL, null=True)
    qualification = models.CharField(max_length=100)
    experience_years = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    is_active = models.BooleanField(default=True)
    profile_picture = models.ImageField(upload_to='doctors/', blank=True, null=True)
    bio = models.TextField(blank=True)
    clinic_address = models.TextField(blank=True)
    available_days = models.CharField(max_length=100, blank=True)
    available_time_start = models.TimeField(blank=True, null=True)
    available_time_end = models.TimeField(blank=True, null=True)
    rating = models.FloatField(default=0.0)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Education(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='educations')
    degree = models.CharField(max_length=100)
    institution = models.CharField(max_length=150)
    year = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.degree} - {self.institution}"


class Certification(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='certifications')
    title = models.CharField(max_length=150)
    issued_by = models.CharField(max_length=150)
    issue_date = models.DateField()
    certificate_file = models.FileField(upload_to='certificates/', blank=True, null=True)

    def __str__(self):
        return self.title


class Specialization(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
