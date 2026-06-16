from django.contrib import admin
from .models import Category, MenuItem
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
admin.site.register(Category, CategoryAdmin)

class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'available', 'category']
    search_fields = ['name', 'category__name']
    list_filter = ['available']
admin.site.register(MenuItem, MenuItemAdmin)