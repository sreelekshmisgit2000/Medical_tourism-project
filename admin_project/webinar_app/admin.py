from django.contrib import admin
from .models import Webinar, WebinarBooking

@admin.register(Webinar)
class WebinarAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'speaker', 'price', 'capacity', 'is_active')
    list_filter = ('is_active', 'date', 'language')
    search_fields = ('title', 'speaker', 'tags', 'description')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('title', 'slug', 'description', 'date', 'speaker', 'price', 'link', 'image', 'duration_minutes', 'capacity', 'registration_deadline', 'recording_url', 'language', 'tags', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(WebinarBooking)
class WebinarBookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'webinar', 'is_paid', 'created_at')
    list_filter = ('is_paid', 'created_at', 'webinar')
    search_fields = ('user__username', 'webinar__title', 'razorpay_order_id', 'razorpay_payment_id')
    readonly_fields = ('created_at',)
