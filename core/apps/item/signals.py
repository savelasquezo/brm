from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Item
from .serializers import ItemSerializer

def getItems():
    """
    Retrieves items that are marked as active.

    Returns:
    list: List of available items.
    """
    Items = Item.objects.filter(is_active=True)
    serializer = ItemSerializer(Items, many=True)
    aviableItems = serializer.data
    return aviableItems

def getAviableItems():
    """
    Retrieves and returns available items.

    Returns:
    list: List of available items.
    """
    aviableItems = getItems()
    return aviableItems
        
@receiver(post_save, sender=Item)
@receiver(post_delete, sender=Item)
def signalItems(sender, instance, **kwargs):
    """
    Signal receiver to send updated item data to WebSocket clients.

    This signal is triggered after an Item instance is saved or deleted.
    It sends a signal to the WebSocket group 'groupItems' with updated available item data.

    Parameters:
    - sender: The sender of the signal (Item in this case).
    - instance: The instance of the sender (Item instance).
    - kwargs: Additional keyword arguments.

    Returns:
    None
    """
    channel_layer = get_channel_layer()
    data = getAviableItems()
    async_to_sync(channel_layer.group_send)(
        "groupItems",
        {
            "type": "asyncSignal",
            "data": data,
        }
    )


