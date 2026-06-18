from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    phone = models.CharField(max_length=15, unique=True, verbose_name='شماره همراه')
    email = models.EmailField(blank=True, null=True, verbose_name='آدرس ایمیل')
    first_name = models.CharField(max_length=100, verbose_name='نام')
    last_name = models.CharField(max_length=100, verbose_name='نام خانوادگی')
    description = models.TextField(blank=True, null=True, verbose_name='توضیحات')
    is_active = models.BooleanField(default=True, verbose_name='فعال')
    is_staff = models.BooleanField(default=False, verbose_name='کارمند')
    is_superuser = models.BooleanField(default=False, verbose_name="ابر کاربر")
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ عضویت')
    
    objects = UserManager()
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = []
    def __str__(self):
        return self.phone