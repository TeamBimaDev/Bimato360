from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .filters import BimaHrPositionFilter
from .models import BimaHrPosition
from .serializers import BimaHrPositionSerializer


class BimaHrPositionViewSet(AbstractViewSet):
    queryset = BimaHrPosition.objects.select_related('department', 'job_category', 'manager').all()
    serializer_class = BimaHrPositionSerializer
    ordering = ["-title"]
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = ['title', 'department__name']
    filterset_class = BimaHrPositionFilter

    action_permissions = {
        'list': ['position.can_read'],
        'create': ['position.can_create'],
        'retrieve': ['position.can_read'],
        'update': ['position.can_update'],
        'partial_update': ['position.can_update'],
        'destroy': ['position.can_delete'],
    }

    def get_object(self):
        obj = BimaHrPosition.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
