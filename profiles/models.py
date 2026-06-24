from django.db import models
from django.conf import settings


class Profile(models.Model):
    name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام ')
    username = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name='نام کاربری')
    picture = models.ImageField(upload_to='product/', blank=True, null=True, verbose_name='عکس پروفایل')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    address = models.TextField(blank=True, null=True, verbose_name='محل سکونت')
    birth_date = models.DateField(blank=True, null=True, verbose_name='تاریخ تولد')
    
    def __str__(self):
        return f"{self.user.phone}"
