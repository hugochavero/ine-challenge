"""
Initial staff user creation command
"""
import os

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = 'Create INE staff user'

    def handle(self, *args, **options):
        try:
            env_staff_user = "INITIAL_STAFF_USERNAME"
            env_staff_email = "INITIAL_STAFF_EMAIL"
            env_staff_pass = "INITIAL_STAFF_PASSWORD"
            username = os.environ[env_staff_user]
            email = os.environ[env_staff_email]
            userpass = os.environ[env_staff_pass]
            os.unsetenv(env_staff_user)
            os.unsetenv(env_staff_email)
            os.unsetenv(env_staff_pass)
        except KeyError:
            self.stdout.write("At least one staff user creation env var were not found. (See README.md)")
            self.stdout.write("Skipping staff user creation.")

        self.stdout.write(f"Creating {username} staff user")

        if User.objects.filter(username=username).exists():
            self.stdout.write(f"User {username} already exists, skipping.")
            return

        user = User.objects.create_superuser(username=username, email=email, password=userpass)
        self.stdout.write(f"Staff user {user.username} created")
        self.stdout.write(f"Add permissions about User model")
        user_content_type = ContentType.objects.get_for_model(User)
        user_model_permissions = Permission.objects.filter(content_type=user_content_type)
        user.user_permissions.add(*user_model_permissions)
        self.stdout.write(f"Permissions assignment done")
