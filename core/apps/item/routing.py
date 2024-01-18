from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    re_path(r"app/ws/items/", consumers.AsyncItemsConsumer.as_asgi()),
]