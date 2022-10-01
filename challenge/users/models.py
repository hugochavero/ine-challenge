import uuid

from django.contrib.auth.models import AbstractUser
from django.db import models

from users.constants import SubscriptionConstants


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, db_index=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    subscription = models.CharField(null=True, max_length=150, choices=SubscriptionConstants.CHOICES)
