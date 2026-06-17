from django.db.models.signals import pre_save
from django.dispatch import receiver
import os
from .models import ProductImage


@receiver(pre_save, sender=ProductImage)
def delete_old_image_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return
    try:
        old_image = ProductImage.objects.get(pk=instance.pk).image
    except ProductImage.DoesNotExist:
        return
    new_image = instance.image
    if old_image and old_image != new_image:
        if os.path.isfile(old_image.path):
            os.remove(old_image.path)