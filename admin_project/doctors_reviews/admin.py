from django.contrib import admin
from .models import Review

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('client_name', 'rating', 'is_active', 'created_at')  # list view columns
    list_filter = ('is_active', 'rating', 'created_at')  # sidebar filters
    search_fields = ('client_name', 'review_text', 'diagnosis')  # search box fields
    ordering = ('-created_at',)  # newest first
    readonly_fields = ('created_at',)  # admin can't edit created_at
