from rest_framework import serializers
import apps.invoice.models as models

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Invoice
        fields = '__all__'

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ItemList
        fields = '__all__'