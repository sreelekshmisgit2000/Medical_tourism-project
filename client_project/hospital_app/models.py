from django.db import models
from doctor_app.models import Doctor
from django.utils.text import slugify

# Create your models here.
class Specialty(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='specialty_icons/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Specialties'

class HospitalType(models.Model):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='hospital_type_icons/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']

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

    title = models.CharField(max_length=255, unique=True)
    authority = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    accreditation_type = models.CharField(max_length=20, choices=ACCREDITATION_TYPE_CHOICES, default='national')
    valid_from = models.DateField(blank=True, null=True)
    valid_to = models.DateField(blank=True, null=True)
    certificate_number = models.CharField(max_length=255, blank=True, null=True)
    document = models.FileField(upload_to='accreditation_documents/', blank=True, null=True)
    website_url = models.URLField(blank=True, null=True)
    contact_person = models.CharField(max_length=255, blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=50, blank=True, null=True)
    renewal_reminder_days = models.PositiveIntegerField(default=90)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Hospital(models.Model):
    # Step 1: Basic Info
    name = models.CharField(max_length=255)
    tagline = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='hospital_logos/', blank=True, null=True)
    cover_image = models.ImageField(upload_to='hospital_covers/', blank=True, null=True)
    year_established = models.CharField(max_length=10, blank=True, null=True)
    hospital_type = models.ForeignKey(HospitalType, on_delete=models.SET_NULL, blank=True, null=True)
    accreditation = models.ForeignKey(Accreditation, on_delete=models.SET_NULL, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    license_number = models.CharField(max_length=100, blank=True, null=True)
    registration_number = models.CharField(max_length=100, blank=True, null=True)
    visiting_hours = models.CharField(max_length=255, blank=True, null=True)
    operating_hours = models.CharField(max_length=255, blank=True, null=True)
    insurance_accepted = models.TextField(blank=True, null=True)
    languages_spoken = models.TextField(blank=True, null=True)
    patient_capacity = models.CharField(max_length=50, blank=True, null=True)
    hospital_features = models.TextField(blank=True, null=True)  # NEW: Hospital features as text
    rating = models.CharField(max_length=10, blank=True, null=True)
    reviews = models.TextField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    parking_available = models.BooleanField(default=False)
    parking_details = models.TextField(blank=True, null=True)
    pharmacy_available = models.BooleanField(default=False)
    blood_bank_available = models.BooleanField(default=False)
    fax_number = models.CharField(max_length=20, blank=True, null=True)
    
    # Step 2: Location & Contact
    state = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    nearby_landmarks = models.TextField(blank=True, null=True)
    map_location = models.TextField(blank=True, null=True)
    latitude = models.CharField(max_length=20, blank=True, null=True)
    longitude = models.CharField(max_length=20, blank=True, null=True)
    primary_contact_number = models.CharField(max_length=20, blank=True, null=True)
    secondary_contact_number = models.CharField(max_length=20, blank=True, null=True)
    phone = models.CharField(max_length=20)  # Keep for backward compatibility
    email = models.EmailField(max_length=255)
    website = models.URLField(blank=True, null=True)
    emergency_contact = models.CharField(max_length=20, blank=True, null=True)
    ambulance_contact = models.CharField(max_length=20, blank=True, null=True)
    
    # Step 3: Ownership & Management
    owned_by = models.CharField(max_length=255, blank=True, null=True)
    ceo_name = models.CharField(max_length=255, blank=True, null=True)
    
    # Step 4: Beds & Rooms
    total_bed_count = models.PositiveIntegerField(blank=True, null=True)
    icu_beds_available = models.BooleanField(default=False)
    icu_beds_count = models.PositiveIntegerField(blank=True, null=True)
    suite_rooms_available = models.BooleanField(default=False)
    suite_rooms_count = models.PositiveIntegerField(blank=True, null=True)
    suite_room_details = models.TextField(blank=True, null=True)
    vip_rooms_available = models.BooleanField(default=False)
    vip_rooms_count = models.PositiveIntegerField(blank=True, null=True)
    vip_room_details = models.TextField(blank=True, null=True)
    emergency_casualty_beds = models.CharField(max_length=10, blank=True, null=True)
    
    # Step 5: Specialties, Treatments, Allied Services
    specialties = models.ManyToManyField(Specialty, related_name='hospitals', blank=True)
    allied_services = models.ManyToManyField('AlliedService', related_name='hospitals', blank=True)
    # Step 6: SEO
    seo_title = models.CharField(max_length=255, blank=True, null=True)
    meta_description = models.TextField(blank=True, null=True)
    keywords = models.TextField(blank=True, null=True)
    slug = models.SlugField(max_length=255, blank=True, null=True, unique=True)
    
    # Legacy fields for backward compatibility
    type = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Active')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

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

    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES, default='laboratory')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    duration_minutes = models.PositiveIntegerField(blank=True, null=True)
    requires_appointment = models.BooleanField(default=True)
    is_emergency_available = models.BooleanField(default=False)
    operating_hours = models.CharField(max_length=255, blank=True)
    contact_number = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class HospitalGallery(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='galleries')
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='hospital/gallery/')
    category = models.CharField(max_length=100, blank=True)  # eg: Operation Theatre, Reception, Labs
    is_featured = models.BooleanField(default=False)
    uploaded_by = models.CharField(max_length=100, blank=True)  # name of uploader/staff
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
class HospitalAward(models.Model):
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='awards')
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    award_date = models.DateField()
    awarded_by = models.CharField(max_length=150)
    award_type = models.CharField(max_length=100, blank=True)  # eg: National, State-level, International
    location = models.CharField(max_length=150, blank=True)    # where the award was given
    image = models.ImageField(upload_to='hospital/awards/', blank=True, null=True)
    certificate_file = models.FileField(upload_to='hospital/awards/certificates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
def save(self, *args, **kwargs):
    if not self.slug and self.name:
        self.slug = self.generate_unique_slug()
    super().save(*args, **kwargs)
    
def generate_unique_slug(name):
    base_slug = slugify(name)
    slug = base_slug
    counter = 1
    while Hospital.objects.filter(slug=slug).exists():
        slug = f"{base_slug}-{counter}"
        counter += 1
    return slug

class BestSurgeon(models.Model):
    hospital = models.ForeignKey(Hospital, related_name='best_surgeons', on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    note = models.CharField(max_length=255, blank=True, null=True)  # Optional description or highlight

    class Meta:
        unique_together = ('hospital', 'doctor')

    def __str__(self):
        return f"{self.doctor.name} - Best Surgeon at {self.hospital.name}"


class BestTreatment(models.Model):
    hospital = models.ForeignKey(Hospital, related_name='best_treatments', on_delete=models.CASCADE, null= True, blank= True)
    treatment = models.ForeignKey('treatment_app.Treatment', on_delete=models.CASCADE)
    note = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        unique_together = ('hospital', 'treatment')

    def __str__(self):
        return f"{self.treatment.title} - Best Treatment at {self.hospital.name}"