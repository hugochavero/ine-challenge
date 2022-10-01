from django.contrib.auth.hashers import check_password, make_password
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from users.constants import (
    PasswordValidationConstants,
    SubscriptionConstants,
    UserSerializerConstants,
)
from users.exceptions import SubscriptionClientException
from users.models import User
from users import subscription_client


class GroupSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=150)

    def to_internal_value(self, data):
        return {"name": data}

    def to_representation(self, instance):
        return instance.name


class BaseSerializer(serializers.ModelSerializer):
    groups = GroupSerializer(many=True)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['password'] = UserSerializerConstants.PASSWORD_MASK
        return representation

    class Meta:
        model = User
        fields = UserSerializerConstants.BASE
        read_only_field = UserSerializerConstants.READ_ONLY


class SmallUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = UserSerializerConstants.SMALL_READ_ONLY
        read_only_field = UserSerializerConstants.SMALL_READ_ONLY


class CreateSerializer(BaseSerializer):
    email = serializers.EmailField(allow_blank=False)
    repeat_password = serializers.CharField(max_length=255, write_only=True)

    class Meta(BaseSerializer.Meta):
        fields = UserSerializerConstants.CREATION
        read_only_field = UserSerializerConstants.READ_ONLY

    @staticmethod
    def _validate_password(attrs) -> None:
        #  Validate password and repeat password match
        if not attrs.get('repeat_password'):
            raise ValidationError({"repeat_password": "This field is required"})
        if attrs.get('password') != attrs.get('repeat_password'):
            raise ValidationError({"password": "password field and repeat_password field must match"})
        del attrs['repeat_password']
        #  Validate regex
        RegexValidator(
            PasswordValidationConstants.REGEX,
            message=PasswordValidationConstants.MESSAGE
        )(attrs['password'])

    @staticmethod
    def _set_subscription_state(user) -> None:
        try:
            response = subscription_client.get_subscription(user.id)
            subscription_state = response["subscription"]
        except SubscriptionClientException:
            subscription_state = SubscriptionConstants.ERROR
        user.subscription = subscription_state
        user.save()

    def _set_user_groups(self, user, groups):
        # Add related groups to user
        if groups:
            _groups = []
            for group in groups:
                _groups.append(Group.objects.get_or_create(**group)[0])
            user.groups.set(_groups)

    def validate(self, attrs):
        self._validate_password(attrs)
        return attrs

    def create(self, validated_data):
        groups = validated_data.pop("groups")
        user = User.objects.create_user(**validated_data)
        self._set_user_groups(user, groups)
        self._set_subscription_state(user)
        return user


class BaseUpdateSerializer(CreateSerializer):
    def update(self, instance, validated_data):
        if validated_data.get("password"):
            validated_data["password"] = make_password(validated_data["password"])
        return super().update(instance, validated_data)


class StaffUpdateSerializer(BaseUpdateSerializer):
    @staticmethod
    def _validate_password(attrs) -> None:
        if attrs.get("password"):
            CreateSerializer._validate_password(attrs)

    def update(self, instance, validated_data):
        groups = validated_data.pop("groups", [])
        self._set_user_groups(instance, groups)
        return super().update(instance, validated_data)


class UserUpdateSerializer(BaseUpdateSerializer):
    old_password = serializers.CharField(max_length=255, write_only=True)
    groups = GroupSerializer(many=True, read_only=True)

    class Meta(BaseSerializer.Meta):
        fields = UserSerializerConstants.CREATION + ["old_password"]
        read_only_field = UserSerializerConstants.READ_ONLY

    @staticmethod
    def _validate_password(attrs) -> None:
        if attrs.get("password") and not attrs.get("old_password"):
            raise ValidationError({"old_password": "You must input old password"})
        CreateSerializer._validate_password(attrs)

    def validate_email(self, value):
        if User.objects.exclude(id=self.instance.id).filter(email=value).exists():
            raise ValidationError(f"The email {value} is already token by other user")
        return value

    def validate_old_password(self, value):
        if not check_password(value, self.instance.password):
            raise ValidationError("Wrong old password")
        return value

