from rest_framework import viewsets


class ShopViewSetMixin(viewsets.ModelViewSet):
    """Manage objects in the database"""

    serializer_class = None
    queryset = None
