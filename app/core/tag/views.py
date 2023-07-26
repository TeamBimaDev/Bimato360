from rest_framework.decorators import action
from rest_framework.response import Response
from core.abstract.views import AbstractViewSet
from common.permissions.action_base_permission import ActionBasedPermission
from .models import BimaCoreTag
from .serializers import BimaCoreTagSerializer


class BimaCoreTagViewSet(AbstractViewSet):
    queryset = BimaCoreTag.objects.all()
    serializer_class = BimaCoreTagSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)

    action_permissions = {
        'list': ['tag.can_read'],
        'create': ['tag.can_create'],
        'retrieve': ['tag.can_read'],
        'update': ['tag.can_update'],
        'partial_update': ['tag.can_update'],
        'destroy': ['tag.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreTag.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=True)
    def all_parents(self, request, pk=None):
        tag = self.get_object()
        parents = []
        parent = tag.parent
        while parent is not None:
            parents.append(BimaCoreTagSerializer(parent).data)
            parent = parent.parent
        return Response(parents)

    @action(detail=True)
    def all_children(self, request, pk=None):
        tag = self.get_object()
        children = []

        def get_children(tag):
            if tag.children.exists():
                for child in tag.children.all():
                    children.append(BimaCoreTagSerializer(child).data)
                    get_children(child)

        get_children(tag)
        return Response(children)

    @action(detail=True, methods=['GET'], url_path='direct_children')
    def direct_children(self, request, pk=None):
        tag = self.get_object()
        direct_children = tag.children.all()
        serializer = BimaCoreTagSerializer(direct_children, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='all_parents_nested')
    def all_parents_nested(self, request, pk=None):
        tag = self.get_object()

        def get_nested_parent(tag):
            if tag.parent is None:
                return None
            else:
                parent_data = get_nested_parent(tag.parent)
                department_serializer_data = self.get_serializer(tag.parent).data
                if parent_data is not None:
                    department_serializer_data['tag'] = parent_data
                return department_serializer_data

        nested_parents = get_nested_parent(tag)
        return Response(nested_parents)
