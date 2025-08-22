from django.contrib import admin
from django.utils.html import format_html
from .models import Doctor, Education, Certification, SpecializationIcon, Specialization

# 🔹 Inline Education in Doctor Admin
class EducationInline(admin.TabularInline):
    model = Education
    extra = 1  # Number of empty rows shown by default

# 🔹 Inline Certification in Doctor Admin
class CertificationInline(admin.TabularInline):
    model = Certification
    extra = 1

# 🔹 Doctor Admin
@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ['name', 'specialization', 'experience_years', 'is_active', 'created_at']
    list_filter = ['is_active', 'specialization', 'gender']
    search_fields = ['name', 'specialization__name', 'qualification']
    inlines = [EducationInline, CertificationInline]
    prepopulated_fields = {"slug": ("name",)}  # Auto-fill slug
    readonly_fields = ['created_at', 'updated_at']  # For reference

# 🔹 Specialization Icon Admin
@admin.register(SpecializationIcon)
class SpecializationIconAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon_preview']
    search_fields = ['name']

    def icon_preview(self, obj):
        if obj.icon:
            return format_html('<img src="{}" width="40" height="40" />', obj.icon.url)
        return "-"
    icon_preview.short_description = 'Icon'

# 🔹 Education Admin
@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'degree', 'institution', 'year']
    search_fields = ['doctor__name', 'degree', 'institution']

# 🔹 Certification Admin
@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    list_display = ['doctor', 'title', 'issued_by', 'issue_date']
    search_fields = ['doctor__name', 'title', 'issued_by']

# 🔹 Specialization Admin
@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
