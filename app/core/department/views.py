from core.abstract.views import AbstractViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from .models import BimaCoreDepartment
from .serializers import BimaCoreDepartmentSerializer
from rest_framework.response import Response
from core.post.models import BimaCorePost
from core.post.serializers import BimaCorePostSerializer
from django.utils.translation import gettext_lazy as _
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreDepartmentViewSet(AbstractViewSet):
    queryset = BimaCoreDepartment.objects.select_related('department').all()
    serializer_class = BimaCoreDepartmentSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['name', 'manager', 'department__name']

    action_permissions = {
        'list': ['department.can_read'],
        'create': ['department.can_create'],
        'retrieve': ['department.can_read'],
        'update': ['department.can_update'],
        'partial_update': ['department.can_update'],
        'destroy': ['department.can_delete'],
    }

    def perform_update(self, serializer):
        self.validate_department(self.request.data)
        serializer.save()

    def validate_department(self, data):
        department_to_edit = self.get_object()
        proposed_parent_id = data.get('department_public_id')

        if not proposed_parent_id:
            return True

        proposed_parent = BimaCoreDepartment.objects.get_object_by_public_id(proposed_parent_id)

        if not proposed_parent or not proposed_parent.department:
            return True

        # Checks for the department that is being updated to not become a child of its own descendant
        def is_descendant(department):
            for child in department.children.all():
                if child.public_id.hex == proposed_parent_id or is_descendant(child):
                    return True
            return False

        if is_descendant(department_to_edit):
            raise ValidationError(_("A department cannot have its descendant as its parent."))

        # Checks for the department that is being updated to not become a parent of its own ancestor
        def is_ancestor(department):
            if department.department is None:
                return False
            if department.department.public_id.hex == data['id'] or is_ancestor(department.department):
                return True
            return False

        if is_ancestor(proposed_parent):
            raise ValidationError(_("A department cannot become a parent of its own ancestor."))

    def get_object(self):
        obj = BimaCoreDepartment.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def get_posts_by_department(self, request, public_id=None):
        department = BimaCoreDepartment.objects.get_object_by_public_id(self.kwargs['public_id'])
        posts = BimaCorePost.objects.filter(department=department)
        serializer = BimaCorePostSerializer(posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='all_parents')
    def all_parents(self, request, pk=None):
        department = self.get_object()
        parents = []
        current_department = department.department
        while current_department is not None:
            print(current_department)
            parents.append(current_department)
            current_department = current_department.department
        serializer = BimaCoreDepartmentSerializer(parents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='all_children')
    def all_children(self, request, pk=None):
        department = self.get_object()

        def get_all_children(department):
            children = []
            for child in department.children.all():
                children.append(child)
                children.extend(get_all_children(child))
            return children

        children = get_all_children(department)
        serializer = BimaCoreDepartmentSerializer(children, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='direct_children')
    def direct_children(self, request, pk=None):
        department = self.get_object()
        children = department.children.all()
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)