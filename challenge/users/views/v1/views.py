from django.contrib.auth.models import User

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from challenge.constants import ViewActions
from users.serializers import BaseSerializer, CreateSerializer


class UsersViewSet(ModelViewSet):
    """

    """
    queryset = User.objects.all()
    serializer_class = BaseSerializer

    def get_serializer_class(self):
        serializer_class = {
            ViewActions.CREATE: CreateSerializer
        }
        return serializer_class.get(self.action, self.serializer_class)
