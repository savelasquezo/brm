import os, uuid
from django.conf import settings
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import status
from rest_framework.response import Response

from . import models, serializers
from apps.item.models import Item

class addItemShopcart(generics.GenericAPIView):
    """
    API endpoint for adding items to the shopping cart.

    Parameters:
    - email (str): The email of the user performing the action.
    - uuid (str): The UUID of the item to be added to the shopping cart.
    - ammount (int): The quantity of the item to be added.

    Request Method: POST

    Returns:
    - 200 OK: If the item is successfully added to the shopping cart.
        Response: {'detail': 'Item Successfully added to ShopCart.'}

    - 400 Bad Request: If there is an error, the item is not found, or the request is malformed.
        Response: {'error': 'NotFound Lottery.'}
    """
    serializer_class = serializers.AddItemSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):

        email = str(request.data.get('email', ''))
        uuid = str(request.data.get('uuid', ''))
        ammount = int(request.data.get('ammount', ''))

        try:
            cart_user = models.UserAccount.objects.get(email=email)
            cart_item = Item.objects.get(uuid=uuid)
            cart_item_price = cart_item.price
            print(f'cart_item_price {cart_item_price}')
            cart_shop = models.ShoppingCart.objects.get(user=cart_user)
            existing_item = models.CartItem.objects.filter(shoppcart=cart_shop, item=cart_item).first()

            if existing_item:
                existing_item.ammount += ammount
                existing_item.price = cart_item_price
                existing_item.save()
            else:
                new_item = models.CartItem.objects.create(shoppcart=cart_shop, item=cart_item, ammount=ammount, price=cart_item_price)
                new_item.save()

            all_items_cart = models.CartItem.objects.filter(shoppcart=cart_shop)
            cart_shop.total = sum(Item.objects.get(uuid=item.item.uuid).price * item.ammount for item in all_items_cart)
            cart_shop.save()

            cart_item.ammount -= ammount
            cart_item.save()
            return Response({'detail': 'Item Succefuly add to ShopCart.'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            date = timezone.now().strftime("%Y-%m-%d %H:%M")
            with open(os.path.join(settings.BASE_DIR, 'logs/core.log'), 'a') as f:
                f.write("addItemShopcart {} --> Error: {}\n".format(date, str(e)))
            return Response({'error': 'NotFound ShoppingCart.'}, status=status.HTTP_400_BAD_REQUEST)


class fetchShopCart(generics.GenericAPIView):
    def get(self, request, *args, **kwargs):
        email = "email@email.com"

        try:
            user = models.UserAccount.objects.get(email=email)
        except models.UserAccount.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        try:
            shopping_cart = models.ShoppingCart.objects.get(user=user)
            cart_items = models.CartItem.objects.filter(shoppcart=shopping_cart)
        except models.ShoppingCart.DoesNotExist:
            return Response({'detail': 'Carrito de compras no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        cart_items_serializer = serializers.CartItemSerializer(cart_items, many=True)
        response_data = {
            'id': shopping_cart.id,
            'last_updated': shopping_cart.last_updated.strftime('%m/%d/%Y'),
            'total': shopping_cart.total,
            'user': str(shopping_cart.user),
            'items': cart_items_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)