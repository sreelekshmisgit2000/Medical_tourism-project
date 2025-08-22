from django.contrib import admin
from .models import CustomUser
from django.contrib.auth.admin import UserAdmin

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_customer', 'is_staff')
    list_filter = ('is_customer', 'is_staff')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_customer',)}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
