from core.abstract.views import AbstractViewSet
from .models import BimaCoreCash
from .serializers import BimaCoreCashSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreCashViewSet(AbstractViewSet):
    queryset = BimaCoreCash.objects.all()
    serializer_class = BimaCoreCashSerializer
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
        obj = BimaCoreCash.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
