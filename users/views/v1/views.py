from django.contrib.auth.models import Permission
from rest_framework.serializers import Serializer
from rest_framework.viewsets import ModelViewSet

from challenge.constants import ViewActions
from users.models import User
from users.permissions import StaffPermission
from users.serializers import (
    BaseSerializer,
    CreateSerializer,
    StaffUpdateSerializer,
    UserUpdateSerializer,
    SmallUserSerializer,
)


class UsersViewSet(ModelViewSet):
    """
    User Main ViewSet
    """

    queryset = User.objects.all()
    serializer_class = SmallUserSerializer

    def get_permissions(self) -> Permission:
        """
        Get permission class according to view action
        :return:
        """
        if self.action in [ViewActions.CREATE, ViewActions.DESTROY]:
            return [StaffPermission()]
        return super().get_permissions()

    def get_serializer_class(self) -> Serializer:
        """
        Get serializer class according vies action and authenticated user
        :return:
        """
        user = self.request.user
        update_serializer = UserUpdateSerializer
        retrieve_serializer = SmallUserSerializer
        if user.is_staff:
            update_serializer = StaffUpdateSerializer
        if user.is_staff or self.kwargs.get("pk") == str(user.id):
            retrieve_serializer = BaseSerializer

        serializer_class = {
            ViewActions.CREATE: CreateSerializer,
            ViewActions.RETRIEVE: retrieve_serializer,
            ViewActions.PARTIAL_UPDATE: update_serializer,
            ViewActions.UPDATE: update_serializer,
        }
        return serializer_class.get(self.action, self.serializer_class)
