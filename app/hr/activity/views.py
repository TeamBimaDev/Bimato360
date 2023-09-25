from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .models import BimaHrActivity
from .serializers import BimaHrActivitySerializer


class BimaHrActivityViewSet(AbstractViewSet):
    queryset = BimaHrActivity.objects.all()
    serializer_class = BimaHrActivitySerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['activity.can_read'],
        'create': ['activity.can_create'],
        'retrieve': ['activity.can_read'],
        'update': ['activity.can_update'],
        'partial_update': ['activity.can_update'],
        'destroy': ['activity.can_delete'],
    }

    def get_object(self):
        obj = BimaHrActivity.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
