from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django_filters import rest_framework as django_filters
from rest_framework import filters

from .models import BimaUserRole
from .serializers import BimaUserRoleSerializer
from .service import filter_passed_permission_return_only_available


class BimaUserRoleViewSet(AbstractViewSet):
    queryset = BimaUserRole.objects.all()
    serializer_class = BimaUserRoleSerializer
    filter_backends = [filters.OrderingFilter, django_filters.DjangoFilterBackend]
    filterset_fields = ['name', 'note']
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + ['name', 'active']

    action_permissions = {
        'list': ['role.can_read'],
        'create': ['role.can_create'],
        'retrieve': ['role.can_read'],
        'update': ['role.can_update'],
        'partial_update': ['role.can_update'],
        'destroy': ['role.can_delete'],
    }

    def get_object(self):
        obj = BimaUserRole.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def perform_create(self, serializer):
        permissions = self.request.data.get('permissions')
        existing_permissions = filter_passed_permission_return_only_available(permissions)
        serializer.save(permissions=existing_permissions)

    def perform_update(self, serializer):
        permissions = self.request.data.get('permissions')
        existing_permissions = filter_passed_permission_return_only_available(permissions)
        role = serializer.save()
        role.permissions.set(existing_permissions)
