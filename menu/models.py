import os
from django.db import models
from django.conf import settings


class Category(models.Model):
    """
    Represents a menu category (e.g. Coffee, Dessert, Cold Drinks).
    Each category can have multiple menu items.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categories"


class MenuItem(models.Model):
    """
    Represents a single item on the cafe menu.
    Each item belongs to one category and can have multiple images.
    """

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class ProductImage(models.Model):
    """
    Represents an image associated with a MenuItem.
    Each item can have multiple images, but only one can be marked as primary.
    When an image is deleted or replaced, the old file is removed from disk.
    """

    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="menu_items/")
    is_primary = models.BooleanField(default=False)

    def __str__(self):
        return f"Image for {self.menu_item.name}"

    def save(self, *args, **kwargs):
        """
        Ensures only one image per MenuItem is marked as primary.
        """
        if self.is_primary:
            ProductImage.objects.filter(
                menu_item=self.menu_item,
                is_primary=True
            ).exclude(pk=self.pk).update(is_primary=False)
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        """
        Deletes the image file from disk when the ProductImage record is deleted.
        """
        if self.image and os.path.isfile(self.image.path):
            os.remove(self.image.path)
        super().delete(*args, **kwargs)

class Wishlist(models.Model):
    """
    Represents a customer's saved/favourite menu items.
    Each customer can have multiple wishlist items.
    """
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='wishlist'
    )
    menu_item = models.ForeignKey(
        MenuItem,
        on_delete=models.CASCADE,
        related_name='wishlisted_by'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('customer', 'menu_item')

    def __str__(self):
        return f"{self.customer.username} - {self.menu_item.name}"        
