"""
Views for the user API.
"""
from django.contrib.auth.models import Permission
from rest_framework import generics, authentication, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

from user.models import User


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system."""
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class CreateTokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user."""
    serializer_class = UserSerializer
    # authentication_classes = [authentication.isA]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return the authenticated user."""
        return self.request.user


class UserPermissionViewSet(viewsets.ViewSet):

    # Custom action for managing user permissions
    @action(detail=True, methods=['post'], url_path='manage-permissions')
    def manage_permissions(self, request, pk=None):
        user = User.objects.get(pk=pk)
        permissions = request.data.get('permissions', [])

        # Add permissions to user
        for perm_codename in permissions.get('add', []):
            permission = Permission.objects.get(codename=perm_codename)
            user.user_permissions.add(permission)

        # Remove permissions from user
        for perm_codename in permissions.get('remove', []):
            permission = Permission.objects.get(codename=perm_codename)
            user.user_permissions.remove(permission)

        return Response({'status': 'Permissions updated successfully'})


class ListPermissionsViewSet(viewsets.ViewSet):

    @action(detail=False, methods=['get'], url_path='get-permissions')
    def get(self, request):
        permissions = Permission.objects.all()
        permissions_list = [{'id': perm.id, 'codename': perm.codename, 'name': perm.name} for perm in permissions]
        return Response(permissions_list)
