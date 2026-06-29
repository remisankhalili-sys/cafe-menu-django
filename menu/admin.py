from django.contrib import admin
from .models import Category, MenuItem, ProductImage, Order, OrderItem


class ManagerPermissionMixin:
    """Mixin to restrict admin access to Manager group or superusers only."""

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


class ProductImageInline(admin.TabularInline):
    """Inline admin for product images within MenuItem."""
    model = ProductImage
    extra = 3
    fields = ['image', 'is_primary']


class OrderItemInline(admin.TabularInline):
    """Inline admin for order items within Order."""
    model = OrderItem
    extra = 0
    fields = ['menu_item', 'quantity', 'price']
    readonly_fields = ['menu_item', 'quantity', 'price']


@admin.register(MenuItem)
class MenuItemAdmin(ManagerPermissionMixin, admin.ModelAdmin):
    """Admin panel for menu items with image inline."""
    inlines = [ProductImageInline]
    list_display = ['name', 'category', 'price', 'is_available']
    list_filter = ['category', 'is_available']
    search_fields = ['name', 'description']


@admin.register(Category)
class CategoryAdmin(ManagerPermissionMixin, admin.ModelAdmin):
    """Admin panel for menu categories."""
    list_display = ['name']


@admin.register(ProductImage)
class ProductImageAdmin(ManagerPermissionMixin, admin.ModelAdmin):
    """Admin panel for product images."""
    list_display = ['menu_item', 'is_primary']


@admin.register(Order)
class OrderAdmin(ManagerPermissionMixin, admin.ModelAdmin):
    """
    Admin panel for orders with filtering by date and category.
    Managers can filter orders by date range and product category.
    """
    inlines = [OrderItemInline]
    list_display = ['id', 'customer', 'status', 'created_at', 'get_total']
    list_filter = ['status', 'created_at', 'items__menu_item__category']
    search_fields = ['customer__username', 'customer__email']
    readonly_fields = ['customer', 'created_at']
    date_hierarchy = 'created_at'

    def get_total(self, obj):
        """Display total price of the order."""
        return f"${obj.get_total()}"
    get_total.short_description = 'Total'
