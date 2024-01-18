import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Item
from .serializers import ItemSerializer

@sync_to_async
def getAsyncItems():
    """
    Asynchronously retrieves items that are marked as active.

    Returns:
    list: List of available items.
    """
    Items = Item.objects.filter(is_active=True)
    serializer = ItemSerializer(Items, many=True)
    aviableItems = serializer.data
    return aviableItems

async def getAsyncAviableItems():
    """
    Asynchronously retrieves and returns available items.

    Returns:
    list: List of available items.
    """
    aviableItems = await getAsyncItems()
    return aviableItems

class AsyncItemsConsumer(AsyncWebsocketConsumer):
    """
    Asynchronous WebSocket consumer for handling item-related data.

    This consumer is designed to work with asynchronous code.

    Methods:
    - async_items: Asynchronously retrieves available items.
    - connect: Handles the WebSocket connection and sends available items to the client.
    - disconnect: Handles the WebSocket disconnection.
    - receive: Placeholder method for receiving WebSocket messages.
    - async_signal: Asynchronously sends a signal containing data to the client.
    """
    async def asyncItems(self):
        """
        Asynchronously retrieves available items.

        Returns:
        list: List of available items.
        """
        data = await getAsyncAviableItems()
        return data

    async def connect(self):
        self.group_name = "groupItems"
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

        data = await self.asyncItems()
        await self.send(json.dumps(data))

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data=None, bytes_data=None):
        pass

    async def asyncSignal(self, event):
        """
        Asynchronously sends a signal containing data to the client.

        Parameters:
        event: The event containing data to be sent.

        Returns:
        None
        """
        data = event['data']
        await self.send(json.dumps(data))