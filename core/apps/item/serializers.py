from rest_framework import serializers
import apps.item.models as models

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Item
        fields = '__all__'