"""
User serializers
"""
from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from users import subscription_client
from users.constants import (
    PasswordValidationConstants,
    SubscriptionConstants,
    UserSerializerConstants,
)
from users.exceptions import SubscriptionClientException
from users.models import User


class GroupSerializer(serializers.Serializer):
    """
    Django group serializer
    """
    name = serializers.CharField(max_length=150)

    def to_internal_value(self, data) -> dict:
        """
        Internal data serialization
        :param data:
        :return:
        """
        return {"name": data}

    def to_representation(self, instance) -> str:
        """
        External serialized data representation
        :param instance:
        :return:
        """
        return instance.name


class BaseSerializer(serializers.ModelSerializer):
    """
    Base user serializer
    """
    groups = GroupSerializer(many=True)

    def to_representation(self, instance) -> dict:
        """
        External serialized data representation
        :param instance:
        :return:
        """
        representation = super().to_representation(instance)
        representation["password"] = UserSerializerConstants.PASSWORD_MASK
        return representation

    class Meta:
        model = User
        fields = UserSerializerConstants.BASE
        read_only_field = UserSerializerConstants.READ_ONLY


class SmallUserSerializer(serializers.ModelSerializer):
    """
    Small user serializer
    """
    class Meta:
        model = User
        fields = UserSerializerConstants.SMALL_READ_ONLY
        read_only_field = UserSerializerConstants.SMALL_READ_ONLY


class CreateSerializer(BaseSerializer):
    """
    Create user serializer
    """
    email = serializers.EmailField(allow_blank=False)
    repeat_password = serializers.CharField(max_length=255, write_only=True)

    class Meta(BaseSerializer.Meta):
        fields = UserSerializerConstants.CREATION
        read_only_field = UserSerializerConstants.READ_ONLY

    @staticmethod
    def _validate_password(attrs) -> None:
        """
        Validate input passwords
        :param attrs:
        :return:
        """
        #  Validate password and repeat password match
        if not attrs.get("repeat_password"):
            raise ValidationError({"repeat_password": "This field is required"})
        if attrs.get("password") != attrs.get("repeat_password"):
            raise ValidationError(
                {"password": "password field and repeat_password field must match"}
            )
        del attrs["repeat_password"]
        #  Validate regex
        RegexValidator(
            PasswordValidationConstants.REGEX,
            message=PasswordValidationConstants.MESSAGE,
        )(attrs["password"])

    @staticmethod
    def _set_subscription_state(user) -> None:
        """
        Get subscription state from subscription service
        :param user:
        :return:
        """
        try:
            response = subscription_client.get_subscription(user.id)
            subscription_state = response["subscription"]
        except SubscriptionClientException:
            subscription_state = SubscriptionConstants.ERROR
        user.subscription = subscription_state
        user.save()

    def _set_user_groups(self, user, groups) -> None:
        """
        Relate group to user
        :param user:
        :param groups:
        :return:
        """
        if groups:
            _groups = []
            for group in groups:
                _groups.append(Group.objects.get_or_create(**group)[0])
            user.groups.set(_groups)

    def validate(self, attrs) -> None:
        """
        Main serializer validation
        :param attrs:
        :return:
        """
        self._validate_password(attrs)
        return attrs

    def create(self, validated_data) -> User:
        """
        Create user, set groups and get subscription state
        :param validated_data:
        :return:
        """
        groups = validated_data.pop("groups")
        user = User.objects.create_user(**validated_data)
        self._set_user_groups(user, groups)
        self._set_subscription_state(user)
        return user


class BaseUpdateSerializer(CreateSerializer):
    """
    Base user serializer
    """
    def update(self, instance, validated_data):
        """
        Base update method
        :param instance:
        :param validated_data:
        :return:
        """
        if validated_data.get("password"):
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class StaffUpdateSerializer(BaseUpdateSerializer):
    """
    Staff user update serializer
    """
    @staticmethod
    def _validate_password(attrs) -> None:
        """
        Staff user password validation
        :param attrs:
        :return:
        """
        if attrs.get("password"):
            CreateSerializer._validate_password(attrs)

    def update(self, instance, validated_data):
        """
        Staff user update
        :param instance:
        :param validated_data:
        :return:
        """
        groups = validated_data.pop("groups", [])
        self._set_user_groups(instance, groups)
        return super().update(instance, validated_data)


class UserUpdateSerializer(BaseUpdateSerializer):
    """
    User update serializer
    """
    old_password = serializers.CharField(max_length=255, write_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta(BaseSerializer.Meta):
        fields = UserSerializerConstants.CREATION + ["old_password"]
        read_only_field = UserSerializerConstants.READ_ONLY

    @staticmethod
    def _validate_password(attrs) -> None:
        """

        :param attrs:
        :return:
        """
        if attrs.get("password"):
            if not attrs.get("old_password"):
                raise ValidationError({"old_password": "You must input old password"})
            CreateSerializer._validate_password(attrs)

    def validate_email(self, value) -> str:
        """

        :param value:
        :return:
        """
        if User.objects.exclude(id=self.instance.id).filter(email=value).exists():
            raise ValidationError(f"The email {value} is already token by other user")
        return value

    def validate_old_password(self, value) -> str:
        """

        :param value:
        :return:
        """
        if not check_password(value, self.instance.password):
            raise ValidationError("Wrong old password")
        return value
