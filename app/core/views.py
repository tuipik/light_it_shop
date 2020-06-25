from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from .mixins import ShopViewSetMixin
from .models import Product, Order, Bill
from .permissions import HasGroupPermission
from .serializers import ProductSerializer, OrderSerializer, BillSerializer
from django_filters import rest_framework as filters


class ProductViewSet(ShopViewSetMixin):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)


class OrderFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ['date']


class OrderViewSet(ShopViewSetMixin):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = OrderFilter
    permission_classes = (IsAuthenticatedOrReadOnly, HasGroupPermission)
    required_groups = {
         'GET': ['all_staff'],
         'POST': ['all_staff'],
         'PUT': ['all_staff'],
     }

    def delete(self, *args, **kwargs):
        return Response({'dich': True})


class BillViewSet(ShopViewSetMixin):
    serializer_class = BillSerializer
    queryset = Bill.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly, HasGroupPermission)
    required_groups = {
         'GET': ['accounter'],
         'POST': ['accounter'],
         'PUT': ['accounter'],
     }
