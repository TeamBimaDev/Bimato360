from core.abstract.views import AbstractViewSet
from .models import BimaCorePost
from .serializers import BimaCorePostSerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCorePostViewSet(AbstractViewSet):
    queryset = BimaCorePost.objects.select_related('department').all()
    serializer_class = BimaCorePostSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'department__name']

    action_permissions = {
        'list': ['post.can_read'],
        'create': ['post.can_create'],
        'retrieve': ['post.can_read'],
        'update': ['post.can_update'],
        'partial_update': ['post.can_update'],
        'destroy': ['post.can_delete'],
    }

    def get_object(self):
        obj = BimaCorePost.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
