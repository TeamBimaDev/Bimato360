"""
Views for the user API.
"""
from django.contrib.auth.models import Permission
from django.db import transaction
from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.settings import api_settings

from user.serializers import (
    UserSerializer,
    AuthTokenSerializer,
)

from user.models import User


class CreateTokenView(TokenObtainPairView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='list-permissions')
    def list_permissions(self, request):
        permissions = Permission.objects.all()
        permissions_list = [{'id': perm.id, 'name': perm.name, 'codename': perm.codename} for perm in permissions]
        return Response(permissions_list)

    @action(detail=False, methods=['post'], url_path='manage-permissions')
    def manage_permissions(self, request):
        # Check if the user has the permission to access this endpoint
        if not request.user.has_perm('auth.change_permission'):
            return Response({'error': 'You do not have permission to manage permissions'},
                            status=status.HTTP_403_FORBIDDEN)

        new_permission_ids = set(request.data.get('permissions', []))
        current_permission_ids = set(request.user.user_permissions.values_list('id', flat=True))

        permissions_to_add = new_permission_ids - current_permission_ids
        permissions_to_remove = current_permission_ids - new_permission_ids

        with transaction.atomic():
            permissions_to_add = Permission.objects.filter(id__in=permissions_to_add)
            request.user.user_permissions.add(*permissions_to_add)

            permissions_to_remove = Permission.objects.filter(id__in=permissions_to_remove)
            request.user.user_permissions.remove(*permissions_to_remove)

        return Response({'status': 'Permissions updated successfully'})
