<<<<<<< HEAD
from core.abstract.views import AbstractViewSet
from core.state.models import BimaCoreState
from core.state.serializers import BimaCoreStateSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreStateViewSet(AbstractViewSet):
    queryset = BimaCoreState.objects.select_related('country').all()
    serializer_class = BimaCoreStateSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'code', 'country__name']

    action_permissions = {
        'list': ['state.can_read'],
        'create': ['state.can_create'],
        'retrieve': ['state.can_read'],
        'update': ['state.can_update'],
        'partial_update': ['state.can_update'],
        'destroy': ['state.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreState.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
=======
from core.abstract.views import AbstractViewSet
from core.state.models import BimaCoreState
from core.state.serializers import BimaCoreStateSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreStateViewSet(AbstractViewSet):
    queryset = BimaCoreState.objects.select_related('country').all()
    serializer_class = BimaCoreStateSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'code', 'country__name']

    action_permissions = {
        'list': ['state.can_read'],
        'create': ['state.can_create'],
        'retrieve': ['state.can_read'],
        'update': ['state.can_update'],
        'partial_update': ['state.can_update'],
        'destroy': ['state.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreState.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
>>>>>>> origin/ma-branch
