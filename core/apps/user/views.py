import os
from django.utils import timezone

from django.conf import settings

from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny

from .models import UserAccount, ShoppingCart, CartItem
from .serializers import AddItemSerializer, ShoppingCartSerializer, CartItemSerializer

from apps.item.models import Item

class addItemShopcart(generics.GenericAPIView):
    """
    View to add an item to the shopping cart.

    This endpoint allows authenticated users to add a specified amount of a given item to their shopping cart.

    Parameters:
    - request (HttpRequest): Django request object.
    - args: Additional non-keyword arguments.
    - kwargs: Additional keyword arguments.

    Returns:
    Response: HTTP response indicating the result of the operation.
    """
    serializer_class = AddItemSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to add an item to the shopping cart.

        Parameters:
        - request (HttpRequest): Django request object.
        - args: Additional non-keyword arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        Response: HTTP response indicating the result of the operation.
        """
        email = str(request.data.get('email', ''))
        uuid = str(request.data.get('uuid', ''))
        ammount = int(request.data.get('ammount', ''))

        try:

            cart_user = UserAccount.objects.get(email=email)
            cart_item = Item.objects.get(uuid=uuid)
            cart_item_price = cart_item.price

            cart_shop = ShoppingCart.objects.get(user=cart_user)
            existing_item = CartItem.objects.filter(shoppcart=cart_shop, item=cart_item).first()

            if existing_item:
                existing_item.ammount += ammount
                existing_item.price = cart_item_price
                existing_item.save()
            else:
                new_item = CartItem.objects.create(shoppcart=cart_shop, item=cart_item, ammount=ammount, price=cart_item_price)
                new_item.save()

            all_items_cart = CartItem.objects.filter(shoppcart=cart_shop)
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
    """
    View to fetch the details of a user's shopping cart.

    This endpoint retrieves information about the user's shopping cart, including the items in the cart.

    Parameters:
    - request (HttpRequest): Django request object.
    - args: Additional non-keyword arguments.
    - kwargs: Additional keyword arguments.

    Returns:
    Response: HTTP response containing the details of the shopping cart.
    """
    serializer_class = ShoppingCartSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to fetch the details of a user's shopping cart.

        Parameters:
        - request (HttpRequest): Django request object.
        - args: Additional non-keyword arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        Response: HTTP response containing the details of the shopping cart.
        """

        try:
            user = UserAccount.objects.get(email=request.user.email)
        except UserAccount.DoesNotExist:
            return Response({'detail': 'Usuario no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        try:
            shopping_cart = ShoppingCart.objects.get(user=user)
            cart_items = CartItem.objects.filter(shoppcart=shopping_cart)
        except ShoppingCart.DoesNotExist:
            return Response({'detail': 'Carrito de compras no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        cart_items_serializer = CartItemSerializer(cart_items, many=True)
        response_data = {
            'id': shopping_cart.id,
            'last_updated': shopping_cart.last_updated.strftime('%m/%d/%Y'),
            'total': shopping_cart.total,
            'user': str(shopping_cart.user),
            'items': cart_items_serializer.data
        }

        return Response(response_data, status=status.HTTP_200_OK)