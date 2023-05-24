from core.abstract.views import AbstractViewSet
from .models import BimaCorePost
from .serializers import BimaCorePostSerializer
from core.department.models import BimaCoreDepartment
from django.shortcuts import get_object_or_404
from django.db.models.query import prefetch_related_objects
from rest_framework import status
from rest_framework.response import Response
from core.pagination import DefaultPagination

class BimaCorePostViewSet(AbstractViewSet):
    queryset = BimaCorePost.objects.all()
    serializer_class = BimaCorePostSerializer
    permission_classes = []
    pagination_class = DefaultPagination

    def create(self, request):
        department_public_id = request.data.get('department')
        department = get_object_or_404(BimaCoreDepartment, public_id=department_public_id)
        data_to_save = request.data
        data_to_save['department_id'] = department.id
        serializer = self.get_serializer(data=data_to_save)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data_to_save = request.data.copy()
        department_public_id = data_to_save.get('department')
        department = get_object_or_404(BimaCoreDepartment, public_id=department_public_id)
        data_to_save['department_id'] = department.id
        serializer = self.get_serializer(instance, data=data_to_save, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
        return Response(serializer.data)

    def get_object(self):
        obj = BimaCorePost.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj


