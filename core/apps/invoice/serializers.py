from rest_framework import serializers

from .models import Invoice, ItemList
from apps.item.serializers import ItemSerializer

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ItemListSerializer(serializers.ModelSerializer):
    details = ItemSerializer(source='item', read_only=True)

    class Meta:
        model = ItemList
        fields = ('invoice', 'item', 'price', 'ammount', 'details')

