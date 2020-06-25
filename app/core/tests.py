import datetime

from django.contrib.auth.models import Group
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Product, Order, Bill
from .serializers import ProductSerializer, OrderSerializer, BillSerializer

PRODUCTS_URL = reverse("core:products-list")
ORDERS_URL = reverse("core:orders-list")
BILLS_URL = reverse("core:bills-list")


def sample_user(
        email="test@testemail.com",
        password="testpass"
):
    return get_user_model().objects.create_user(email, password)


def create_product(**params):
    defaults = {
        "title": "Some Product",
        "price": 1234,
    }
    defaults.update(params)

    return Product.objects.create(**defaults)


def create_order(**params):
    product = create_product()
    defaults = {
        "product": product,
        "date": datetime.date.today(),
    }
    defaults.update(params)

    return Order.objects.create(**defaults)


def create_bill(order):
    return Bill.objects.create(order=order)


class UserTests(TestCase):
    def test_create_user_with_email_successful(self):
        email = "test@testemail.com"
        password = "Testpass123"
        user = get_user_model().objects.create_user(
            email=email, password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_invalid_email(self):
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")


class ShopApiTests(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@testemail.com", "testpass"
        )
        self.client.force_authenticate(self.user)

        # Group setup
        group_name = "accounter"
        self.group = Group(name=group_name)
        self.group.save()
        group_name = "all_staff"
        self.group = Group(name=group_name)
        self.group.save()

    def add_user_to_permission_group(self, group_name):
        group = Group.objects.get(name=group_name)
        self.user.groups.add(group)

    def test_retrieve_products(self):
        create_product()
        create_product()

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_orders(self):
        self.add_user_to_permission_group('all_staff')
        create_order()

        res = self.client.get(ORDERS_URL)

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_bills(self):
        self.add_user_to_permission_group('accounter')
        order = create_order()
        create_bill(order)

        res = self.client.get(BILLS_URL)

        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_discount_added(self):
        self.add_user_to_permission_group('accounter')
        PRICE = 15142
        DISCIUNT = 3028.4
        SUM_W_DISCOUNT = 12113.6
        product = create_product(price=PRICE)
        order = create_order(product=product,
                             date=datetime.date.today()+datetime.timedelta(31))
        create_bill(order)
        res = self.client.get(BILLS_URL)
        self.assertEqual(float(res.data[0]['discount']), DISCIUNT)
        self.assertEqual(float(res.data[0]['total_price']), SUM_W_DISCOUNT)
