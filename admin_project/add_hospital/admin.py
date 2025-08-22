from django.contrib import admin
from .models import HospitalGallery, HospitalAward

@admin.register(HospitalGallery)
class HospitalGalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'is_featured', 'uploaded_by', 'uploaded_at')
    search_fields = ('title', 'category', 'uploaded_by')
    list_filter = ('is_featured', 'category')

@admin.register(HospitalAward)
class HospitalAwardAdmin(admin.ModelAdmin):
    list_display = ('title', 'award_date', 'award_type', 'awarded_by', 'location')
    search_fields = ('title', 'awarded_by', 'award_type')
    list_filter = ('award_type', 'award_date')
