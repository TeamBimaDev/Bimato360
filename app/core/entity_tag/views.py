<<<<<<< HEAD
from core.abstract.views import AbstractViewSet
from core.entity_tag.models import BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreEntityTagViewSet(AbstractViewSet):
    queryset = BimaCoreEntityTag.objects.select_related('tag').all()
    serializer_class = BimaCoreEntityTagSerializer
    # permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['id_manager', 'order']

    # action_permissions = {
    #     'list': ['entity_tag.can_read'],
    #     'create': ['entity_tag.can_create'],
    #     'retrieve': ['entity_tag.can_read'],
    #     'update': ['entity_tag.can_update'],
    #     'partial_update': ['entity_tag.can_update'],
    #     'destroy': ['entity_tag.can_delete'],
    # }

    def get_object(self):
        obj = BimaCoreEntityTag.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
=======
from core.abstract.views import AbstractViewSet
from core.entity_tag.models import BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreEntityTagViewSet(AbstractViewSet):
    queryset = BimaCoreEntityTag.objects.select_related('tag').all()
    serializer_class = BimaCoreEntityTagSerializer
    # permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['id_manager', 'order']

    # action_permissions = {
    #     'list': ['entity_tag.can_read'],
    #     'create': ['entity_tag.can_create'],
    #     'retrieve': ['entity_tag.can_read'],
    #     'update': ['entity_tag.can_update'],
    #     'partial_update': ['entity_tag.can_update'],
    #     'destroy': ['entity_tag.can_delete'],
    # }

    def get_object(self):
        obj = BimaCoreEntityTag.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
>>>>>>> origin/ma-branch
