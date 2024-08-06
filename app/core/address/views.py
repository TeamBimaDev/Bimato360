from core.abstract.views import AbstractViewSet
from core.address.models import BimaCoreAddress
from core.address.serializers import BimaCoreAddressSerializer

from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreAddressViewSet(AbstractViewSet):
    queryset = BimaCoreAddress.objects.select_related('state', 'country').all()
    serializer_class = BimaCoreAddressSerializer
    # permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['number', 'street', 'city']

    # action_permissions = {
    #     'list': ['address.can_read'],
    #     'create': ['address.can_create'],
    #     'retrieve': ['address.can_read'],
    #     'update': ['address.can_update'],
    #     'partial_update': ['address.can_update'],
    #     'destroy': ['address.can_delete'],
    # }

    def get_object(self):
        obj = BimaCoreAddress.objects. \
            get_object_by_public_id(self.kwargs['pk'])
        return obj
