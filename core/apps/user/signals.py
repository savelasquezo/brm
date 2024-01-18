from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import UserAccount, ShoppingCart

@receiver(post_save, sender=UserAccount)
def create_user_shopcart(sender, instance, created, **kwargs):
    """
    Signal receiver to create a shopping cart for a newly created user account.

    This signal is triggered after a UserAccount instance is saved. If the user account is newly created,
    a corresponding shopping cart is created for that user.

    Parameters:
    - sender: The sender of the signal (UserAccount in this case).
    - instance: The instance of the sender (UserAccount instance).
    - created (bool): Indicates whether the instance was just created.
    - kwargs: Additional keyword arguments.

    Returns:
    None
    """
    if created:
        ShoppingCart.objects.create(user=instance)

