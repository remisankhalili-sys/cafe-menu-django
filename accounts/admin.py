from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Customer


@admin.register(Customer)
class CustomerAdmin(UserAdmin):
    """Admin panel for Customer model."""
    list_display = ['username', 'email', 'phone_number', 'is_staff', 'is_superuser']
    fieldsets = UserAdmin.fieldsets + (
        ('Extra Info', {'fields': ('phone_number', 'profile_picture')}),
    )