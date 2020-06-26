import datetime
from freezegun import freeze_time

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


def detail_url(reversed_url, id):
    return reverse(reversed_url, args=[id])


def sample_user(email="test@testemail.com", password="testpass"):
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
    defaults = {"product": product}
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
        group_names = ["accounter", "all_staff"]
        for name in group_names:
            group = Group(name=name)
            group.save()

    def add_user_to_permission_group(self, group_name):
        for name in group_name:
            group = Group.objects.get(name=name)
            self.user.groups.add(group)

    def test_retrieve_products(self):
        self.add_user_to_permission_group(["accounter", "all_staff"])
        create_product()
        create_product()

        res = self.client.get(PRODUCTS_URL)

        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_orders(self):
        self.add_user_to_permission_group(["all_staff"])
        create_order()

        res = self.client.get(ORDERS_URL)

        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_bills(self):
        self.add_user_to_permission_group(["accounter", "all_staff"])
        order = create_order()
        create_bill(order)

        res = self.client.get(BILLS_URL)

        bills = Bill.objects.all()
        serializer = BillSerializer(bills, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_discount_added(self):
        self.add_user_to_permission_group(["accounter", "all_staff"])
        PRICE = 15142
        DISCIUNT = 3028.4
        SUM_W_DISCOUNT = 12113.6
        product = create_product(price=PRICE)
        with freeze_time(datetime.date.today() + datetime.timedelta(31)):
            order = create_order(product=product,)
        create_bill(order)
        res = self.client.get(BILLS_URL)
        self.assertEqual(float(res.data[0]["discount"]), DISCIUNT)
        self.assertEqual(float(res.data[0]["total_price"]), SUM_W_DISCOUNT)

    def test_bills_cant_see_and_modify_with_all_staff_permission(self):
        self.add_user_to_permission_group(["all_staff"])
        order = create_order()
        create_bill(order)

        res = self.client.get(BILLS_URL)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_can_modify_order_with_all_stuff_permission(self):
        self.add_user_to_permission_group(["all_staff"])
        order = create_order()
        url = f"{ORDERS_URL}{order.id}/"

        res = self.client.put(url, {"is_done": True})

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertTrue(res.data["is_done"])

    def test_filter_orders_by_creation_date(self):
        """
        Test filering by date.
        Creates 6 orders  with different dates, then filters
        from the second one to one before the last
        Result of filtering should be 4
        """
        self.add_user_to_permission_group(["all_staff"])
        order_dates_count = 6
        filtered_orders_count = 4
        dates_list = [
            datetime.date.today() + datetime.timedelta(num)
            for num in range(order_dates_count)
        ]
        for date in dates_list:
            with freeze_time(date):
                create_order()

        res = self.client.get(
            f"{ORDERS_URL}?creation_date_after={dates_list[1]}"
            f"&creation_date_before={dates_list[-2]}"
        )

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), filtered_orders_count)
