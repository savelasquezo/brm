from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from .models import Item
from .serializers import ItemSerializer

def getItems():
    Items = Item.objects.filter(is_active=True)
    serializer = ItemSerializer(Items, many=True)
    aviableItems = serializer.data
    return aviableItems

def getAviableItems():
    aviableItems = getItems()
    return aviableItems
        
@receiver(post_save, sender=Item)
@receiver(post_delete, sender=Item)
def signalItems(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    data = getAviableItems()
    async_to_sync(channel_layer.group_send)(
        "groupItems",
        {
            "type": "asyncSignal",
            "data": data,
        }
    )


