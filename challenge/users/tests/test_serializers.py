from unittest import mock

import pytest
from django.contrib.auth.models import Group
from django.core.exceptions import ValidationError as DjangoValidationError
from pytest_mock import mocker
from rest_framework.exceptions import ValidationError

from users.clients import SubscriptionClient
from users.constants import SubscriptionConstants, UserSerializerConstants
from users.models import User
from users.serializers import CreateSerializer, BaseSerializer


class TestUserCreateSerializer:

    def test_validate_password_not_match(self):
        attrs = {
            "password": 1234,
            "repeat_password": 12345
        }
        serializer = CreateSerializer()
        with pytest.raises(ValidationError):
            serializer._validate_password(attrs)

    def test_validate_password_not_regex(self):
        attrs = {
            "password": "INEine2022",
            "repeat_password": "INEine2022"
        }
        serializer = CreateSerializer()
        with pytest.raises(DjangoValidationError):
            serializer._validate_password(attrs)

    def test_validate_password_ok(self):
        attrs = {
            "password": "Ine*c0nt4at3m3",
            "repeat_password": "Ine*c0nt4at3m3"
        }
        serializer = CreateSerializer()
        assert serializer._validate_password(attrs) is None

    def test_set_subscription_state(self):
        user = User(id=1234)
        user.save = mock.Mock()
        serializer = CreateSerializer()
        serializer._set_subscription_state(user)
        assert user.subscription == SubscriptionConstants.ACTIVE
        user.save.assert_called()

    @pytest.mark.django_db
    def test_set_user_groups(self):
        user = User.objects.create()
        groups = [{"name": "group1"}, {"name": "group2"}]

        serializer = CreateSerializer()
        serializer._set_user_groups(user, groups)
        assert user.groups.count() == 2

    def test_validate(self):
        serializer = CreateSerializer()
        serializer._validate_password = mock.Mock()
        serializer.validate({})
        serializer._validate_password.assert_called()

    @mock.patch('users.models.User.objects.create_user')
    def test_create(self, mocked_create_user):
        user_data = {
            "username": "username",
            "groups": []
        }
        serializer = CreateSerializer()
        serializer._set_user_groups = mock.Mock()
        serializer._set_subscription_state = mock.Mock()
        serializer.create(user_data)
        mocked_create_user.assert_called()
        serializer._set_user_groups.assert_called()
        serializer._set_subscription_state.assert_called()

    @pytest.mark.django_db
    def test_to_representation(self):
        user = User(password=123456)
        serializer = BaseSerializer()
        result = serializer.to_representation(user)
        assert result["password"] == UserSerializerConstants.PASSWORD_MASK
