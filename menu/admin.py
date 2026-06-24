from django.contrib import admin

from django.contrib.auth.models import User
from .models import Category, MenuItem, ProductImage


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'is_primary']


@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ['name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']

    def has_module_perms(self, request):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

    def has_module_perms(self, request):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    def has_add_permission(self, request):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    def has_change_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.groups.filter(name='Manager').exists() or request.user.is_superuser


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ['menu_item', 'is_primary']
    
    def save(self, *args, **kwargs):
        if self.is_primary:
            ProductImage.objects.filter(
                menu_item=self.menu_item,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)
