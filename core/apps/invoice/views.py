import os
from django.conf import settings
from django.utils import timezone

from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .models import Invoice, ItemList
from .serializers import InvoiceSerializer, ItemListSerializer

from apps.user.models import UserAccount, ShoppingCart, CartItem


class fetchInvoiceItems(generics.GenericAPIView):
    """
    View to fetch items from the latest invoice of a user.

    This endpoint retrieves and returns the items from the latest invoice associated with a specified user.

    Parameters:
    - request (HttpRequest): Django request object.
    - args: Additional non-keyword arguments.
    - kwargs: Additional keyword arguments.

    Returns:
    Response: HTTP response containing the details of the latest invoice and its associated items.
    """
    serializer_class = ItemListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to fetch items from the latest invoice of a user.

        Parameters:
        - request (HttpRequest): Django request object.
        - args: Additional non-keyword arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        Response: HTTP response containing the details of the latest invoice and its associated items.
        """

        uemail = "email@email.com"


        try:
            invoice_user = UserAccount.objects.get(email=uemail)
        
            invoices = Invoice.objects.filter(client=invoice_user)
            last_invoice = invoices.latest('id')
            invoice_items = ItemList.objects.filter(invoice__in=invoices)
            serializer = self.serializer_class(invoice_items, many=True)

            response_data = {
                'last_updated': last_invoice.date_sold.strftime('%m/%d/%Y'),
                'user':last_invoice.client.email,
                'items': serializer.data
            }

            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            date = timezone.now().strftime("%Y-%m-%d %H:%M")
            with open(os.path.join(settings.BASE_DIR, 'logs/core.log'), 'a') as f:
                f.write("fetchInvoiceItems {} --> Error: {}\n".format(date, str(e)))
            return Response({'error': 'NotFound fetchInvoiceItems.'}, status=status.HTTP_400_BAD_REQUEST)

class requestInvoice(generics.GenericAPIView):
    """
    View to create a new invoice for a user's shopping cart.

    This endpoint creates a new invoice for the items in a user's shopping cart.

    Parameters:
    - request (HttpRequest): Django request object.
    - args: Additional non-keyword arguments.
    - kwargs: Additional keyword arguments.

    Returns:
    Response: HTTP response indicating the result of the operation.
    """

    serializer_class = InvoiceSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to create a new invoice for a user's shopping cart.

        Parameters:
        - request (HttpRequest): Django request object.
        - args: Additional non-keyword arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        Response: HTTP response indicating the result of the operation.
        """
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
