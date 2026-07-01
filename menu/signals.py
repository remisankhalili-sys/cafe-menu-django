from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Order, Notification
from menu.models import ProductImage


@receiver(post_save, sender=Order)
def create_order_notification(sender, instance, created, **kwargs):
    """Create a notification when a new order is placed."""
    if created:
        Notification.objects.create(
            message=f"New order #{instance.pk} by {instance.customer.username}"
        )


@receiver(pre_save, sender=ProductImage)
def delete_old_image(sender, instance, **kwargs):
    """Delete old image file from disk when a new image is uploaded."""
    if not instance.pk:
        return
    try:
        old_image = ProductImage.objects.get(pk=instance.pk)
    except ProductImage.DoesNotExist:
        return
    if old_image.image != instance.image:
        import os
        if os.path.isfile(old_image.image.path):
            os.remove(old_image.image.path)