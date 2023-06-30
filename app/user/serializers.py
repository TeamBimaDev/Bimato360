"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.password_validation import validate_password
from django.utils.encoding import force_str
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User
from datetime import timedelta
from django.utils import timezone
from django.utils.http import urlsafe_base64_decode


class UserSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='public_id',
                               read_only=True, format='hex')
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['id', 'email', 'name', 'is_active', 'is_staff', 'public_id', 'date_joined',
                  'is_approved', 'approved_by', 'approved_at', 'password']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    approved_by = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['approved_at'] = instance.approved_at.strftime(
            '%Y-%m-%d %H:%M:%S') if instance.approved_at else None
        return representation

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(AuthTokenSerializer, cls).get_token(user)
        # Add custom claims
        token['name'] = user.name
        token['email'] = user.email
        token['user_id'] = user.id
        token['user_public_id'] = user.public_id.hex
        return token


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

    class Meta:
        fields = ['password', 'confirm_password', 'token', 'uidb64']

    def validate(self, attrs):
        try:
            password = attrs.get('password')
            confirm_password = attrs.get('confirm_password')
            uidb64 = attrs.get('uidb64')
            token = attrs.get('token')
            if password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match"})

            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

            # Check that token matches and has not expired
            token_matches = user.reset_password_token == token
            token_not_expired = timezone.now() - user.reset_password_time <= timedelta(hours=24)

            if not token_matches or not token_not_expired:
                raise serializers.ValidationError({'password': 'Token is not valid or has expired'})

            # Clear the token and uid
            user.reset_password_token = None
            user.reset_password_uid = None
            user.reset_password_time = None
            user.save()

            return attrs
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError({'password': 'Reset password failed'})

    def validate_password(self, value):
        validate_password(value.strip())
        return value.strip()
