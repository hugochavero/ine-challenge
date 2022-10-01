from django.conf import settings
from .clients import SubscriptionClient, SubscriptionClientTest

if settings.DEBUG:
    subscription_client = SubscriptionClientTest()
else:
    subscription_client = SubscriptionClient()
