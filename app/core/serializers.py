import datetime

from rest_framework import serializers
from .models import Product, Bill, Order
from django.conf import settings


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "id",
            "title",
            "price",
            "creation_date",
        )
        read_only_fields = ("id",)


class OrderSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "product",
            "product_id",
            "creation_date",
            "is_done",
        )
        read_only_fields = ("id",)


class BillSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)
    order_id = serializers.IntegerField(write_only=True)

    discount = serializers.SerializerMethodField(read_only=True)
    total_price = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Bill
        fields = (
            "id",
            "order",
            "order_id",
            "discount",
            "total_price",
            "creation_date",
            "is_paid",
        )
        read_only_fields = ("id",)

    def is_discount_required(self, obj):
        return (obj.order.product.creation_date + datetime.timedelta(
            settings.DISCOUNT_MONTH_COUNT *
            settings.YEAR_DAYS_COUNT /
            settings.YEAR_MONTH_COUNT)) \
               < obj.order.creation_date

    def discount_amount(self, obj):
        return obj.order.product.price * settings.DISCOUNT_SUM

    def get_discount(self, obj):
        if self.is_discount_required(obj):
            return f"{self.discount_amount(obj):.2f}"
        else:
            return 0

    def get_total_price(self, obj):
        if self.is_discount_required(obj):
            return f"{obj.order.product.price - self.discount_amount(obj):.2f}"
        else:
            return f"{obj.order.product.price:.2f}"
