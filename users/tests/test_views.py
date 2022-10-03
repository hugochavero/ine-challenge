from unittest import mock

import pytest

from challenge.constants import ViewActions
from users.models import User
from users.permissions import StaffPermission
from users.serializers import (
    CreateSerializer,
    BaseSerializer,
    SmallUserSerializer,
    UserUpdateSerializer,
    StaffUpdateSerializer,
)
from users.views.v1 import UsersViewSet


class TestUsersViewSet:

    def test_get_permissions_staff(self):
        view = UsersViewSet()
        view.action = ViewActions.CREATE
        permission_class = view.get_permissions()[0]
        assert isinstance(permission_class, StaffPermission)

    @mock.patch('users.views.v1.views.ModelViewSet.get_permissions')
    def test_get_permissions_normal(self, mocked_super):
        view = UsersViewSet()
        view.action = ViewActions.RETRIEVE
        view.get_permissions()
        mocked_super.assert_called()

    @pytest.mark.parametrize(
        "action, user_staff, view_kwargs, expected_class",
        [
            (ViewActions.RETRIEVE, True, {'pk': '5'}, BaseSerializer),
            (ViewActions.RETRIEVE, False, {'pk': '10'}, BaseSerializer),
            (ViewActions.RETRIEVE, False, {'pk': '5'}, SmallUserSerializer),
            (ViewActions.CREATE, False, {'pk': '5'}, CreateSerializer),
            (ViewActions.PARTIAL_UPDATE, False, {'pk': '5'}, UserUpdateSerializer),
            (ViewActions.PARTIAL_UPDATE, True, {'pk': '5'}, StaffUpdateSerializer),
            (ViewActions.UPDATE, False, {'pk': '5'}, UserUpdateSerializer),
            (ViewActions.UPDATE, True, {'pk': '5'}, StaffUpdateSerializer),
         ]
    )
    def test_get_serializer_class(self, action, user_staff, view_kwargs, expected_class):
        mocked_request = mock.Mock()
        mocked_request.user = User(is_staff=user_staff, id=10)
        view = UsersViewSet()
        view.request = mocked_request
        view.action = action
        view.kwargs = view_kwargs
        serializer_class = view.get_serializer_class()
        assert serializer_class == expected_class
