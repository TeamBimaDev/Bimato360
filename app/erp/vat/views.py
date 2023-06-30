from core.abstract.views import AbstractViewSet
from .models import BimaErpVat
from .serializers import BimaErpVatSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaErpVatViewSet(AbstractViewSet):
    queryset = BimaErpVat.objects.all()
    serializer_class = BimaErpVatSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['vat.can_read'],
        'create': ['vat.can_create'],
        'retrieve': ['vat.can_read'],
        'update': ['vat.can_update'],
        'partial_update': ['vat.can_update'],
        'destroy': ['vat.can_delete'],
    }

    def get_object(self):
        obj = BimaErpVat.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
