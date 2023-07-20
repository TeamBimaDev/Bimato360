from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from django.utils.translation import gettext_lazy as _
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

    def validate_parent(self, data):
        tag_to_edit = self.get_object()
        proposed_parent_id = data.get('parent_public_id')

        if not proposed_parent_id:
            return True

        proposed_parent = BimaCoreTag.objects.get_object_by_public_id(proposed_parent_id)

        if not proposed_parent or not proposed_parent.parent:
            return True

        def is_descendant(tag):
            for child in tag.children.all():
                if child.public_id.hex == proposed_parent_id or is_descendant(child):
                    return True
            return False

        if is_descendant(tag_to_edit):
            raise ValidationError({"Error": _("A tag cannot have its descendant as its parent.")})

    def perform_update(self, serializer):
        self.validate_parent(self.request.data)
        serializer.save()

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
