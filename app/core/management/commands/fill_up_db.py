from django.contrib.auth.management.commands import createsuperuser

from core.models import Product, Order, Bill


class Command(createsuperuser.Command):
    help = "Create a superuser and fill up db with test data"

    def fill_up_db(self):
        for i in range(10):
            product = Product.objects.create(
                title=f"Sample Product {i}",
                price=1000+i
            )
            order = Order.objects.create(
                product=product,
            )
            bill = Bill.objects.create(
                order=order
            )

    def handle(self, *args, **options):
        user_data = {
            "email": "test1@testemail.com",
            "password": "test_pass",
        }

        user = self.UserModel._default_manager.create_superuser(**user_data)

        self.fill_up_db(user)
