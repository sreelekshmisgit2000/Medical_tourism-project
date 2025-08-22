from django.contrib import admin
from .models import Hospital, HospitalGallery
from .models import BestSurgeon,BestTreatment
from doctor_app.models import Doctor

class FacilityImageInline(admin.TabularInline):
    model = HospitalGallery
    extra = 1

class HospitalAdmin(admin.ModelAdmin):
    inlines = [FacilityImageInline]

class BestSurgeonAdmin(admin.ModelAdmin):
    list_display = ['id', 'doctor', 'hospital', 'note']
    search_fields = ['doctor__name', 'hospital__name']
    list_filter = ['hospital']

admin.site.register(BestSurgeon, BestSurgeonAdmin)

admin.site.register(Hospital, HospitalAdmin)
admin.site.register(HospitalGallery)
admin.site.register(BestTreatment)
