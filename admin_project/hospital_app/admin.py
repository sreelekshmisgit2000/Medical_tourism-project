# hospital_app/admin.py

from django.contrib import admin
from .models import (
    Treatment, TreatmentCategory, AlliedService, Accreditation,
    TreatmentSchedule, TreatmentEquipment, ServiceSchedule, AccreditationRenewal
)

@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'treatment_type', 'cost', 'status', 'is_active')
    list_filter = ('treatment_type', 'status', 'is_active', 'requires_anesthesia', 'requires_room')
    search_fields = ('name', 'description', 'category')
    ordering = ('name',)


@admin.register(TreatmentCategory)
class TreatmentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category_type', 'is_active', 'is_featured')
    list_filter = ('category_type', 'is_active', 'is_featured')
    search_fields = ('name', 'description')
    ordering = ('display_order', 'name')


@admin.register(AlliedService)
class AlliedServiceAdmin(admin.ModelAdmin):
    list_display = ('name', 'service_type', 'cost', 'status', 'is_active')
    list_filter = ('service_type', 'status', 'is_active', 'requires_appointment', 'is_emergency_available')
    search_fields = ('name', 'description', 'location')
    ordering = ('name',)


@admin.register(Accreditation)
class AccreditationAdmin(admin.ModelAdmin):
    list_display = ('title', 'authority', 'status', 'valid_from', 'valid_to', 'is_active')
    list_filter = ('accreditation_type', 'status', 'is_active')
    search_fields = ('title', 'authority', 'description', 'certificate_number')
    ordering = ('-valid_to', 'title')


@admin.register(TreatmentSchedule)
class TreatmentScheduleAdmin(admin.ModelAdmin):
    list_display = ('treatment', 'day_of_week', 'start_time', 'end_time', 'is_available')  
    list_filter = ('day_of_week', 'is_available')
    search_fields = ('treatment__name',)


@admin.register(TreatmentEquipment)
class TreatmentEquipmentAdmin(admin.ModelAdmin):
    list_display = ('treatment', 'equipment_name', 'equipment_type', 'is_required', 'quantity_needed')
    list_filter = ('equipment_type', 'is_required')
    search_fields = ('equipment_name',)


@admin.register(ServiceSchedule)
class ServiceScheduleAdmin(admin.ModelAdmin):
    list_display = ('service', 'day_of_week', 'start_time', 'end_time', 'is_available')
    list_filter = ('day_of_week', 'is_available')
    search_fields = ('service__name',)


@admin.register(AccreditationRenewal)
class AccreditationRenewalAdmin(admin.ModelAdmin):
    list_display = ('accreditation', 'renewal_date', 'status', 'documents_submitted', 'fees_paid')
    list_filter = ('status', 'documents_submitted', 'fees_paid')
    search_fields = ('accreditation__title',)
