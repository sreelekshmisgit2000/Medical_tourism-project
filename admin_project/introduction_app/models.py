from django.db import models

class Introduction(models.Model):
    title = models.CharField(max_length=255, default="Introduction")
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Symptoms(models.Model):
    title = models.CharField(max_length=255, default="Symptoms")
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class RiskFactors(models.Model):
    title = models.CharField(max_length=255, default="Risk Factors")
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PreparationOfSurgery(models.Model):
    title = models.CharField(max_length=255, default="Preparation of Surgery")
    content = models.TextField()
    checklist = models.TextField(blank=True, help_text="Comma-separated checklist items")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Procedure(models.Model):
    title = models.CharField(max_length=255, default="Procedure")
    content = models.TextField()
    steps = models.TextField(blank=True, help_text="Comma-separated steps")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class PostProcedure(models.Model):
    title = models.CharField(max_length=255, default="Post Procedure")
    content = models.TextField()
    care_instructions = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class SuccessRate(models.Model):
    title = models.CharField(max_length=255, default="Success Rate")
    content = models.TextField()
    percentage = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)
    reference = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class FAQs(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question

class TopDoctors(models.Model):
    name = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    experience_years = models.IntegerField()
    description = models.TextField(blank=True)
    photo = models.ImageField(upload_to='doctors/', blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class TopHospitals(models.Model):
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    logo = models.ImageField(upload_to='hospitals/', blank=True, null=True)
    contact_info = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name