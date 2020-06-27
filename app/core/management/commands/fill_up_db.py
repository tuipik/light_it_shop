import datetime as d

from django.contrib.auth.management.commands import createsuperuser
from django.contrib.auth import get_user_model

from django.contrib.auth.models import Group

from freezegun import freeze_time

from core.models import Product, Order, Bill


class Command(createsuperuser.Command):
    help = "Create a superuser and fill up db with test data"

    def fill_up_db(self):
        for i in range(10):
            with freeze_time(d.date.today() - d.timedelta(35)):
                product = Product.objects.create(
                    title=f"Sample Product {i}", price=1000 + i
                )
            with freeze_time(d.date.today() - d.timedelta(10 - i)):
                order = Order.objects.create(product=product,)
            Bill.objects.create(order=order)

    def create_staff_user(self, email, password, group_name):
        user = get_user_model().objects.create_user(email, password)
        for name in group_name:
            group = Group.objects.get(name=name)
            user.groups.add(group)
        return user

    def create_groups(self):
        group_names = ["accounter", "all_staff"]
        for name in group_names:
            group = Group(name=name)
            group.save()

    def handle(self, *args, **options):
        superuser_data = {
            "email": "test@testemail.com",
            "password": "test_pass",
        }

        self.UserModel._default_manager.create_superuser(**superuser_data)

        self.fill_up_db()
        self.create_groups()
        staff_users_data = [
            {
                "email": "accounter@a.com",
                "password": "test_pass",
                "group_name": ["accounter", "all_staff"],
            },
            {
                "email": "cashier@a.com",
                "password": "test_pass",
                "group_name": ["accounter", "all_staff"],
            },
            {
                "email": "assistant@a.com",
                "password": "test_pass",
                "group_name": ["all_staff"],
            },
        ]
        for user in staff_users_data:
            self.create_staff_user(**user)
