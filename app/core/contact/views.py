from core.abstract.views import AbstractViewSet
from core.contact.models import BimaCoreContact
from core.contact.serializers import BimaCoreContactSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreContactViewSet(AbstractViewSet):
    queryset = BimaCoreContact.objects.all()
    serializer_class = BimaCoreContactSerializer
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'position']

    action_permissions = {
        'list': ['contact.can_read'],
        'create': ['contact.can_create'],
        'retrieve': ['contact.can_read'],
        'update': ['contact.can_update'],
        'partial_update': ['contact.can_update'],
        'destroy': ['contact.can_delete'],
    }


    def get_object(self):
        obj = BimaCoreContact.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
