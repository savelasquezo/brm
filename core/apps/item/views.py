from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Item
from .serializers import ItemSerializer


class fetchItems(generics.ListAPIView):
    """
    View to fetch a list of available items.

    This endpoint returns a list of items that are marked as active.

    Parameters:
    - request (HttpRequest): Django request object.
    - args: Additional non-keyword arguments.
    - kwargs: Additional keyword arguments.

    Returns:
    Response: HTTP response containing the list of available items.
    """
    queryset = Item.objects.filter(is_active=True)
    serializer_class = ItemSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to fetch a list of available items.

        Parameters:
        - request (HttpRequest): Django request object.
        - args: Additional non-keyword arguments.
        - kwargs: Additional keyword arguments.

        Returns:
        Response: HTTP response containing the list of available items.
        """
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'NotFound Items.'}, status=status.HTTP_404_NOT_FOUND)
                            
  