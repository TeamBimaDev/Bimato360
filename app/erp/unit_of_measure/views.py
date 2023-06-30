from core.abstract.views import AbstractViewSet
from .models import BimaErpUnitOfMeasure
from .serializers import BimaErpUnitOfMeasureSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaErpUnitOfMeasureViewSet(AbstractViewSet):
    queryset = BimaErpUnitOfMeasure.objects.all()
    serializer_class = BimaErpUnitOfMeasureSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['unit_of_measure.can_read'],
        'create': ['unit_of_measure.can_create'],
        'retrieve': ['unit_of_measure.can_read'],
        'update': ['unit_of_measure.can_update'],
        'partial_update': ['unit_of_measure.can_update'],
        'destroy': ['unit_of_measure.can_delete'],
    }

    def get_object(self):
        obj = BimaErpUnitOfMeasure.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
