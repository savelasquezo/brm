from rest_framework import serializers
from .models import Invoice, ItemList

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = '__all__'

class ItemListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemList
        fields = '__all__'