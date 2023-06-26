"""
Serializers for the user API View.
"""
from django.contrib.auth import (
    get_user_model,
)
from django.contrib.auth.password_validation import validate_password
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

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
        return token

"""change and reset password"""
class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_password = serializers.CharField(write_only=True, required=True)
    confirm_new_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'new_password', 'confirm_new_password')

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError("New password fields didn't match.")
        return attrs

    def update(self, instance, validated_data):
        old_password = validated_data.get('old_password')
        new_password = validated_data.get('new_password')

        if old_password and new_password:
            if not instance.check_password(old_password):
                raise serializers.ValidationError("Old password is not correct.")
            instance.set_password(new_password)
            instance.save()
            return instance

        raise serializers.ValidationError("Both old password and new password are required.")