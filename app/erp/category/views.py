from core.abstract.views import AbstractViewSet
from django.db.models import prefetch_related_objects
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from .models import BimaErpCategory
from .serializers import BimaErpCategorySerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination


class BimaErpCategoryViewSet(AbstractViewSet):
    queryset = BimaErpCategory.objects.all()
    serializer_class = BimaErpCategorySerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = []
    pagination_class = DefaultPagination

    def create(self, request):
        category_public_id = request.data.get('category', None)
        category = None
        data_to_save = request.data.copy()

        if category_public_id is not None:
            category = get_object_or_404(BimaErpCategory, public_id=category_public_id)

        if category:
            data_to_save['category_id'] = category.id
            data_to_save['category'] = category.id

        serializer = self.get_serializer(data=data_to_save)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data_to_save = request.data.copy()

        if data_to_save.get('category'):
            category_public_id = data_to_save.get('category')
            category = get_object_or_404(BimaErpCategory, public_id=category_public_id)
            data_to_save['category_id'] = category.id

        serializer = self.get_serializer(instance, data=data_to_save, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        queryset = self.filter_queryset(self.get_queryset())
        if queryset._prefetch_related_lookups:
            instance._prefetched_objects_cache = {}
            prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
        return Response(serializer.data)

    def get_object(self):
        obj = BimaErpCategory.objects.get_object_by_public_id(self.kwargs['pk'])
        # self.check_object_permissions(self.request, obj)
        return obj
