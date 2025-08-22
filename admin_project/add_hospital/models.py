from django.db import models






class HospitalGallery(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='hospital/gallery/')
    category = models.CharField(max_length=100, blank=True)  
    is_featured = models.BooleanField(default=False)
    uploaded_by = models.CharField(max_length=100, blank=True)  
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class HospitalAward(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True)
    award_date = models.DateField()
    awarded_by = models.CharField(max_length=150)
    award_type = models.CharField(max_length=100, blank=True)  
    location = models.CharField(max_length=150, blank=True)    
    image = models.ImageField(upload_to='hospital/awards/', blank=True, null=True)
    certificate_file = models.FileField(upload_to='hospital/awards/certificates/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
