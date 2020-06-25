import datetime
from decimal import Decimal

from rest_framework import serializers, permissions
from .models import Product, Bill, Order


DISCOUNT_SUM = Decimal(0.2)  # 20%


class ProductSerializer(serializers.ModelSerializer):

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "price",
            "date",
        )
        read_only_fields = ("id",)


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    order_date = serializers.DateField(source="date")
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Order
        fields = (
            "id",
            "product",
            "order_date",
            "is_done",
        )
        read_only_fields = ("id",)


class BillSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    bill_date = serializers.DateField(source="date")
    discount = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    class Meta:
        model = Bill
        fields = (
            "id",
            "order",
            "discount",
            "total_price",
            "bill_date",
            "is_paid",
        )
        read_only_fields = ("id",)

    def is_product_old(self, obj):
        return (obj.order.product.date + datetime.timedelta(1 * 365 / 12)) \
               < obj.order.date

    def make_discount(self, obj):
        return obj.order.product.price * DISCOUNT_SUM

    def get_discount(self, obj):
        if self.is_product_old(obj):
            return self.make_discount(obj)
        else:
            return 0

    def get_total_price(self, obj):
        if self.is_product_old(obj):
            return obj.order.product.price - self.make_discount(obj)
        else:
            return obj.order.product.price
