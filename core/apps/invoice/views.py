import os
from django.conf import settings
from django.utils import timezone

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from rest_framework import status
from rest_framework.response import Response

from .models import Invoice, ItemList
from .serializers import InvoiceSerializer, ItemListSerializer

from apps.user.models import UserAccount, ShoppingCart, CartItem

class requestInvoice(generics.GenericAPIView):
    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        email = str(request.data.get('email', ''))

        try:
            client_user = UserAccount.objects.get(email=email)
            client_cart = ShoppingCart.objects.get(user=client_user)
            total_invoice = client_cart.total

            if not client_cart.items.exists():
                return Response({'error': 'NotFound requestInvoice.'}, status=status.HTTP_400_BAD_REQUEST)

            new_invoice = Invoice.objects.create(client=client_user, total=total_invoice)
            new_invoice.save()

            items_in_cart = CartItem.objects.filter(shoppcart=client_cart)

            for obj in items_in_cart:
                item_list = ItemList.objects.create(
                    invoice=new_invoice,
                    item=obj.item,
                    price=obj.price,
                    ammount=obj.ammount
                )
                item_list.save()

            client_cart.total = 0
            client_cart.save()
            client_cart.items.clear()

            return Response({'detail': 'Invoice Succefuly created.'}, status=status.HTTP_200_OK)
        
        except Exception as e:
            date = timezone.now().strftime("%Y-%m-%d %H:%M")
            with open(os.path.join(settings.BASE_DIR, 'logs/core.log'), 'a') as f:
                f.write("requestInvoice {} --> Error: {}\n".format(date, str(e)))
            return Response({'error': 'NotFound requestInvoice.'}, status=status.HTTP_400_BAD_REQUEST)
