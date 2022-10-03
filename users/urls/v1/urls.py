"""
User's v1 urls
"""
from django.urls import path, include
from rest_framework import routers

from users.views.v1 import UsersViewSet

router = routers.DefaultRouter()
router.register(r"users", UsersViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
