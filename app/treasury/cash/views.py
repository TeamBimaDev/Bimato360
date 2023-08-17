from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .models import BimaTreasuryCash
from .serializers import BimaTreasuryCashSerializer


class BimaTreasuryCashViewSet(AbstractViewSet):
    queryset = BimaTreasuryCash.objects.all()
    serializer_class = BimaTreasuryCashSerializer
    permission_classes = (ActionBasedPermission,)

    action_permissions = {
        'list': ['cash.can_read'],
        'create': ['cash.can_create'],
        'retrieve': ['cash.can_read'],
        'update': ['cash.can_update'],
        'partial_update': ['cash.can_update'],
        'destroy': ['cash.can_delete'],
    }

    def get_object(self):
        obj = BimaTreasuryCash.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
