from django.contrib.auth.models import AbstractUser
from django.db import models


class Customer(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    Adds phone number and profile picture to the default user fields.
    Default fields inherited: username, email, password, first_name, last_name
    """

    phone_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True
    )
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customer_set',
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customer_set',
        blank=True
    )

    def __str__(self):
        return self.username