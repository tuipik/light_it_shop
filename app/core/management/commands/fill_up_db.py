from django.contrib.auth.management.commands import createsuperuser

from random import randint
from core.models import Post, Comment


class Command(createsuperuser.Command):
    help = "Create a superuser and fill up db with test data"

    def fill_up_db(self, user):
        for i in range(10):
            post = Post.objects.create(
                title=f"{randint(100, 1000)} Lorem ipsum dolor sit amet",
                link=f"http://{randint(100, 1000)}_test_url.com",
                author=user,
            )
            Comment.objects.create(
                author=user,
                content="Lorem ipsum dolor sit amet, consectetur adipiscing, "
                "sed do eiumod tempor incididunt ut bore dolore magna aliqua.",
                post=post,
            )

    def handle(self, *args, **options):
        user_data = {
            "username": "test_user",
            "password": "test_pass",
            "email": "test@testemail.com",
        }

        user = self.UserModel._default_manager.create_superuser(**user_data)

        self.fill_up_db(user)
