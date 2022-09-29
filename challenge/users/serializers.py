from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer, CharField

from users.constants import UserSerializerFields


class BaseSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = UserSerializerFields.BASE
        read_only_field = UserSerializerFields.READ_ONLY


class CreateSerializer(BaseSerializer):
    repeat_password = CharField(max_length=255)

    def validate(self, attrs):
        if attrs['password'] != attrs['repeat_password']:
            raise ValidationError("Password must be equal")

    class Meta(BaseSerializer.Meta):
        fields = UserSerializerFields.CREATION
        read_only_field = UserSerializerFields.READ_ONLY


class UpdateSerializer(BaseSerializer):
    pass
