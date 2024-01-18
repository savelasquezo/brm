from django.urls import re_path
from .consumers import AsyncItemsConsumer

websocket_urlpatterns = [
    re_path(r"app/ws/items/", AsyncItemsConsumer.as_asgi()),
]