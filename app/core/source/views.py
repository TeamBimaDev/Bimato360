from core.abstract.views import AbstractViewSet
from core.source.models import BimaCoreSource
from core.source.serializers import BimaCoreSourceSerializer

from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreSourceViewSet(AbstractViewSet):
    queryset = BimaCoreSource.objects.all()
    serializer_class = BimaCoreSourceSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name']

    action_permissions = {
        'list': ['source.can_read'],
        'create': ['source.can_create'],
        'retrieve': ['source.can_read'],
        'update': ['source.can_update'],
        'partial_update': ['source.can_update'],
        'destroy': ['source.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreSource.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
