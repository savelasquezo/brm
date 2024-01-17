from django.conf import settings

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from rest_framework import status
from rest_framework.response import Response

from . import models, serializers


class fetchItems(generics.ListAPIView):
    """
    Endpoint to retrieve details of the currently active items.
    Requires no authentication.
    """
    queryset = models.Item.objects.filter(is_active=True)
    serializer_class = serializers.ItemSerializer
    permission_classes = [AllowAny]

    def get(self, request, *args, **kwargs):
        try:
            queryset = self.filter_queryset(self.get_queryset())
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            return Response({'detail': 'NotFound Items.'}, status=status.HTTP_404_NOT_FOUND)
                            
  