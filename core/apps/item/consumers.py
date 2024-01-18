import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from django.core.serializers import serialize

from .models import Item
from .serializers import ItemSerializer

@sync_to_async
def getAsyncItems():
    Items = Item.objects.filter(is_active=True)
    serializer = ItemSerializer(Items, many=True)
    aviableItems = serializer.data
    return aviableItems

async def getAsyncAviableItems():
    aviableItems = await getAsyncItems()
    return aviableItems

class AsyncItemsConsumer(AsyncWebsocketConsumer):

    async def asyncItems(self):
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
        data = event['data']
        await self.send(json.dumps(data))