from django.contrib import admin
from .models import TimeSlot

@admin.register(TimeSlot)
class TimeSlotAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'date', 'start_time', 'end_time', 'status', 'is_active']
    list_filter = ['status', 'is_active', 'date', 'doctor']
    search_fields = ['doctor__name', 'date']
    date_hierarchy = 'date'
    ordering = ['date', 'start_time']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('doctor', 'date', 'start_time', 'end_time')
        }),
        ('Status', {
            'fields': ('status', 'is_active')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('doctor')
