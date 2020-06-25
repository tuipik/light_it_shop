from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly


class ShopViewSetMixin(viewsets.ModelViewSet):
    """Manage objects in the database"""

    serializer_class = None
    queryset = None
