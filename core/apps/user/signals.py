from django.db.models.signals import post_save
from django.dispatch import receiver

from . import models

@receiver(post_save, sender=models.UserAccount)
def create_user_shopcart(sender, instance, created, **kwargs):
    if created:
        models.ShoppingCart.objects.create(user=instance)

