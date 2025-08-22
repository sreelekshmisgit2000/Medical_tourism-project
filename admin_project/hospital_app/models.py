# hospital_app/models.py
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator



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
        ('discontinued', 'Discontinued'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True)
    treatment_type = models.CharField(max_length=20, choices=TREATMENT_TYPE_CHOICES, default='consultation')
    duration_days = models.IntegerField(null=True, blank=True)
    duration_hours = models.IntegerField(null=True, blank=True, help_text="Duration in hours for shorter treatments")
    cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    insurance_coverage = models.BooleanField(default=False, help_text="Whether this treatment is covered by insurance")
    requires_anesthesia = models.BooleanField(default=False)
    requires_room = models.BooleanField(default=False, help_text="Whether this treatment requires a hospital room")
    preparation_instructions = models.TextField(blank=True, help_text="Instructions for patient preparation")
    post_treatment_care = models.TextField(blank=True, help_text="Post-treatment care instructions")
    risk_factors = models.TextField(blank=True, help_text="Potential risks and complications")
    success_rate = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, 
                                     validators=[MinValueValidator(0), MaxValueValidator(100)],
                                     help_text="Success rate percentage")
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']


class TreatmentCategory(models.Model):
    CATEGORY_TYPE_CHOICES = [
        ('medical', 'Medical'),
        ('surgical', 'Surgical'),
        ('diagnostic', 'Diagnostic'),
        ('therapeutic', 'Therapeutic'),
        ('preventive', 'Preventive'),
        ('emergency', 'Emergency'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_TYPE_CHOICES, default='medical')
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    icon = models.CharField(max_length=50, blank=True, help_text="CSS icon class or icon name")
    color_code = models.CharField(max_length=7, blank=True, help_text="Hex color code for UI display")
    is_featured = models.BooleanField(default=False, help_text="Whether this category should be featured on homepage")
    display_order = models.IntegerField(default=0, help_text="Order for display in lists")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['display_order', 'name']
        verbose_name_plural = "Treatment Categories"


class AlliedService(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('laboratory', 'Laboratory'),
        ('radiology', 'Radiology'),
        ('pharmacy', 'Pharmacy'),
        ('physiotherapy', 'Physiotherapy'),
        ('nutrition', 'Nutrition'),
        ('counseling', 'Counseling'),
        ('transport', 'Transport'),
        ('housekeeping', 'Housekeeping'),
        ('security', 'Security'),
        ('maintenance', 'Maintenance'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Under Maintenance'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, default='laboratory')
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    duration_minutes = models.IntegerField(null=True, blank=True, help_text="Estimated duration in minutes")
    requires_appointment = models.BooleanField(default=True, help_text="Whether this service requires prior appointment")
    is_emergency_available = models.BooleanField(default=False, help_text="Whether this service is available for emergencies")
    operating_hours = models.CharField(max_length=100, blank=True, help_text="e.g., Mon-Fri 8AM-6PM")
    contact_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=200, blank=True, help_text="Department or floor location")
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['service_type', 'name']




class Accreditation(models.Model):
    ACCREDITATION_TYPE_CHOICES = [
        ('national', 'National'),
        ('international', 'International'),
        ('state', 'State'),
        ('specialty', 'Specialty'),
        ('quality', 'Quality'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending'),
        ('suspended', 'Suspended'),
        ('revoked', 'Revoked'),
    ]
    
    title = models.CharField(max_length=150, unique=True)
    authority = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    accreditation_type = models.CharField(max_length=20, choices=ACCREDITATION_TYPE_CHOICES, default='national')
    valid_from = models.DateField()
    valid_to = models.DateField()
    certificate_number = models.CharField(max_length=100, unique=True)
    document = models.FileField(upload_to='accreditation_docs/', blank=True, null=True)
    website_url = models.URLField(blank=True, help_text="Official website of the accrediting authority")
    contact_person = models.CharField(max_length=100, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    renewal_reminder_days = models.IntegerField(default=90, help_text="Days before expiry to send reminder")
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, help_text="Additional notes or requirements")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-valid_to', 'title']


class TreatmentSchedule(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
  
    day_of_week = models.IntegerField(choices=[(i, day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])])
    start_time = models.TimeField()
    end_time = models.TimeField()
    max_patients = models.IntegerField(default=10)
    is_available = models.BooleanField(default=True)


class TreatmentEquipment(models.Model):
    treatment = models.ForeignKey(Treatment, on_delete=models.CASCADE)
    equipment_name = models.CharField(max_length=100)
    equipment_type = models.CharField(max_length=50)
    is_required = models.BooleanField(default=True)
    quantity_needed = models.IntegerField(default=1)


class ServiceSchedule(models.Model):
    service = models.ForeignKey(AlliedService, on_delete=models.CASCADE)
    day_of_week = models.IntegerField(choices=[(i, day) for i, day in enumerate(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])])
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_available = models.BooleanField(default=True)


class AccreditationRenewal(models.Model):
    accreditation = models.ForeignKey(Accreditation, on_delete=models.CASCADE)
    renewal_date = models.DateField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed'), ('overdue', 'Overdue')])
    documents_submitted = models.BooleanField(default=False)
    fees_paid = models.BooleanField(default=False)
    notes = models.TextField(blank=True)

