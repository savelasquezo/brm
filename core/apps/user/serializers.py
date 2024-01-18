from djoser.serializers import PasswordResetConfirmSerializer
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()

class UserSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ["username","email","password","is_staff"]

class CustomPasswordResetConfirmSerializer(PasswordResetConfirmSerializer):
    def build_password_reset_confirm_url(self, uid, token):
        url = f"?forgot_password_confirm=True&uid={uid}&token={token}"
        return url

class ShoppingCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ShoppingCart
        fields = '__all__'

##class CartItemSerializer(serializers.ModelSerializer):
##    class Meta:
##        model = models.CartItem
##        fields = '__all__'


class CartItemSerializer(serializers.Serializer):
    email = serializers.EmailField()
    uuid = serializers.UUIDField()
    ammount = serializers.IntegerField()

    def validate(self, data):
        email = data.get('email')
        uuid = data.get('uuid')
        ammount = data.get('ammount')

        if not models.UserAccount.objects.filter(email=email).exists():
            raise serializers.ValidationError({'error': 'UserAccount not found.'})

        if not models.Item.objects.filter(uuid=uuid).exists():
            raise serializers.ValidationError({'error': 'Item not found.'})

        return data