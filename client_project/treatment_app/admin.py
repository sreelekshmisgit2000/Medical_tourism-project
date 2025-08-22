from django.contrib import admin
from .models import Treatment, TreatmentDetail, TreatmentIntro, TreatmentCategory  # ✅ Added TreatmentCategory

@admin.register(TreatmentCategory)
class TreatmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}  # ✅ Auto-fill slug from name
    search_fields = ['name']


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'rating']  # ✅ Show category
    search_fields = ['title', 'description']
    filter_horizontal = ['doctors', 'hospitals']
    list_filter = ['category']
    prepopulated_fields = {'slug': ('title',)}  # ✅ Auto-fill slug from title


@admin.register(TreatmentDetail)
class TreatmentDetailAdmin(admin.ModelAdmin):
    list_display = ['treatment']
    fields = ['treatment', 'description', 'header_image']


@admin.register(TreatmentIntro)
class TreatmentIntroAdmin(admin.ModelAdmin):
    list_display = ['treatment']
    fields = [
        'treatment',
        'introduction',
        'before_image',
        'after_image',
        'stay_info',
        'duration_info',
        'anesthesia_info',
        'cost_info'
    ]
