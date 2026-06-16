from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    
    def __str__(self):
        
        return self.name
    
class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    image = models.ImageField(upload_to='menu_images/', blank=True, null=True)
    available = models.BooleanField(default=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')
    
    def __str__(self):
        return self.name 
    class Meta:
        ordering = ['category', 'name']
        
        indexes = [
            models.Index(fields=['category', 'available'], name='ca_idx'),
            models.Index(fields=['price'], name='price_idx'),
            ]