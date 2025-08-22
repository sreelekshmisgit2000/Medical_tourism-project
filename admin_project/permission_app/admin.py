from django.contrib import admin
from .models import PermissionModelRegistry, ModelPermission

@admin.register(PermissionModelRegistry)
class PermissionModelRegistryAdmin(admin.ModelAdmin):
    list_display = ['model_name']
    search_fields = ['model_name']
    readonly_fields = ['app_label']
    exclude = ['app_label']

@admin.register(ModelPermission)  # ✅ Only one registration
class ModelPermissionAdmin(admin.ModelAdmin):
    list_display = ['user', 'permission_model', 'can_create', 'can_read', 'can_update', 'can_delete']
    list_filter = ['can_create', 'can_read', 'can_update', 'can_delete']
    search_fields = ['user__username', 'permission_model__name']
