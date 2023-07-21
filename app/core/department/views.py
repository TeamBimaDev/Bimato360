from rest_framework.response import Response
from rest_framework.decorators import action

from core.abstract.views import AbstractViewSet
from core.post.models import BimaCorePost
from core.post.serializers import BimaCorePostSerializer

from .models import BimaCoreDepartment
from .serializers import BimaCoreDepartmentSerializer


class BimaCoreDepartmentViewSet(AbstractViewSet):
    queryset = BimaCoreDepartment.objects.select_related('department').all()
    serializer_class = BimaCoreDepartmentSerializer
    ordering_fields = AbstractViewSet.ordering_fields + ['name', 'manager', 'department__name']

    def get_object(self):
        """ Override get_object to retrieve object by public_id """
        return BimaCoreDepartment.objects.get_object_by_public_id(self.kwargs['pk'])

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
            parents.append(current_department)
            current_department = current_department.department
        serializer = self.get_serializer(parents, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='all_parents_nested')
    def all_parents_nested(self, request, pk=None):
        department = self.get_object()

        def get_nested_parent(department):
            if department.department is None:
                return None
            else:
                parent_data = get_nested_parent(department.department)
                department_serializer_data = self.get_serializer(department.department).data
                if parent_data is not None:
                    department_serializer_data['department'] = parent_data
                return department_serializer_data

        nested_parents = get_nested_parent(department)
        return Response(nested_parents)

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
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='direct_children')
    def direct_children(self, request, pk=None):
        department = self.get_object()
        children = department.children.all()
        serializer = self.get_serializer(children, many=True)
        return Response(serializer.data)
