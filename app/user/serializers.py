"""
Serializers for the user API View.
"""
import binascii

from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from .service import verify_user_credential_when_change_password
from datetime import timedelta
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode
from django.utils.translation import gettext_lazy as _


def password_match_validator(data):
    password = data.get('password')
    confirm_password = data.get('confirm_password')
    if password != confirm_password:
        raise ValidationError("Password fields didn't match.")
    return data


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id',
                               read_only=True, format='hex')
    confirm_password = serializers.CharField(write_only=True, required=False)

    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'is_active', 'is_staff', 'public_id', 'date_joined',
                  'is_approved', 'approved_by', 'approved_at', 'password', 'confirm_password']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 5, 'validators': [validate_password]},
        }

    approved_by = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )

    def get_fields(self, *args, **kwargs):
        fields = super().get_fields(*args, **kwargs)
        request = self.context.get('request', None)
        if request and getattr(request, 'method', None) == "PUT":
            fields['password'].required = False
            fields['confirm_password'].required = False
        return fields

    def validate(self, data):
        request_method = self.context['request'].method
        if request_method == "POST":
            password = data.get('password')
            confirm_password = data.get('confirm_password')
            if password != confirm_password:
                raise serializers.ValidationError("Password fields didn't match.")
            if password:
                validate_password(password)
        return data

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['approved_at'] = instance.approved_at.strftime(
            '%Y-%m-%d %H:%M:%S') if instance.approved_at else None
        return representation

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        validated_data.pop('confirm_password', None)
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AdminCreateUserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id', read_only=True, format='hex')

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name']
        extra_kwargs = {'name': {'required': True}}

    def create(self, validated_data):
        """Create and return a new user."""
        password = get_user_model().objects.make_random_password()
        user = get_user_model().objects.create_user(**validated_data, password=password, created_by_admin=True)
        user.is_password_change_when_created = False
        user.created_by_admin = True
        user.set_password(password)
        user.save()
        return user


class AuthTokenSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        if not user.is_active or not user.is_approved:
            raise serializers.ValidationError(_("User is not active or not approved."))

        return data

    @classmethod
    def get_token(cls, user):
        token = super(AuthTokenSerializer, cls).get_token(user)
        token['name'] = user.name
        token['email'] = user.email
        token['user_id'] = user.id
        token['user_public_id'] = user.public_id.hex
        token['permissions'] = get_custom_user_permissions(user)
        return token


def get_custom_user_permissions(user):
    permissions = user.user_permissions.all()
    return [p.codename for p in permissions]


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    new_password_confirm = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({"new_password": "New passwords fields didn't match."})
        return attrs

    def validate_new_password(self, value):
        validate_password(value)
        return value


class ResetPasswordEmailRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(min_length=2)

    class Meta:
        fields = ['email']

    def validate_email(self, value):
        try:
            user = get_user_model().objects.get(email=value)
        except get_user_model().DoesNotExist:
            raise serializers.ValidationError('User with this email does not exists.')
        return value


class SetNewPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    confirm_password = serializers.CharField(min_length=6, max_length=68, write_only=True)
    token = serializers.CharField(min_length=1, write_only=True, required=False)
    uidb64 = serializers.CharField(min_length=1, write_only=True, required=False)
    public_id = serializers.UUIDField()

    class Meta:
        fields = ['password', 'confirm_password', 'token', 'uidb64', 'public_id']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')
            public_id = attrs.get('public_id')

            if password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

            error, _ = verify_user_credential_when_change_password(uidb64, token, public_id)

            if error:
                raise serializers.ValidationError(error)

            user = User.objects.get(public_id=public_id)

            user.reset_password_token = None
            user.reset_password_uid = None
            user.reset_password_time = None
            user.set_password(password)
            if user.is_password_change_when_created is False:
                user.is_password_change_when_created = True
                user.is_approved = True
                user.approved_at = timezone.now()
            user.save()

            return attrs
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'password': 'Reset password failed'})

    def validate_password(self, value):
        validate_password(value.strip())
        return value.strip()
