from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def __str__(self):
        return self.username
