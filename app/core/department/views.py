from core.abstract.views import AbstractViewSet
from rest_framework.exceptions import ValidationError

from .models import BimaCoreDepartment
from .serializers import BimaCoreDepartmentSerializer
from rest_framework.response import Response
from core.post.models import BimaCorePost
from core.post.serializers import BimaCorePostSerializer
from django.utils.translation import gettext_lazy as _
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreDepartmentViewSet(AbstractViewSet):
    queryset = BimaCoreDepartment.objects.select_related('department').prefetch_related('children__children').all()
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
        department_to_edit = BimaCoreDepartment.objects.get_object_by_public_id(data['id'])

        if data.get('department_public_id') is None:
            return True

        department_child = BimaCoreDepartment.objects.get_object_by_public_id(data['department_public_id'])
        if department_child is None:
            return True

        if department_child.department is None:
            return True

        if (
                (data['department_public_id'] == department_child.public_id.hex) and \
                (department_child.department.public_id.hex == data['id'])
        ):
            raise ValidationError(_("A department cannot have its parent as its child."))

    def get_object(self):
        obj = BimaCoreDepartment.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def get_posts_by_department(self, request, public_id=None):
        department = BimaCoreDepartment.objects.get_object_by_public_id(self.kwargs['public_id'])
        posts = BimaCorePost.objects.filter(department=department)
        serializer = BimaCorePostSerializer(posts, many=True)
        return Response(serializer.data)
