from django.db import models




class Review(models.Model):
    client_name = models.CharField(max_length=100)
    review_text = models.TextField()
    rating = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    diagnosis = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)  

    def __str__(self):
        return f"{self.client_name} - {self.rating} stars"

