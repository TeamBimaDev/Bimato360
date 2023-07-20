import django_filters
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.http import JsonResponse
from django.utils.translation import gettext_lazy as _
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework import status
from rest_framework.response import Response

from core.entity_tag.models import get_entity_tags_for_parent_entity, create_single_entity_tag, BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from core.abstract.views import AbstractViewSet
from common.permissions.action_base_permission import ActionBasedPermission
from .models import BimaErpCategory
from .serializers import BimaErpCategorySerializer


class CategoryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.ChoiceFilter(choices=[('True', 'True'), ('False', 'False'), ('all', 'all')],
                                         method='filter_active')

    class Meta:
        model = BimaErpCategory
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all':
            return queryset
        else:
            return queryset.filter(active=(value == 'True'))


class BimaErpCategoryViewSet(AbstractViewSet):
    queryset = BimaErpCategory.objects.all()
    serializer_class = BimaErpCategorySerializer
    filterset_class = CategoryFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['category.can_read'],
        'create': ['category.can_create'],
        'retrieve': ['category.can_read'],
        'update': ['category.can_update'],
        'partial_update': ['category.can_update'],
        'destroy': ['category.can_delete'],
    }

    def validate_category(self, data):
        category_to_edit = self.get_object()
        proposed_parent_id = data.get('category_public_id')

        if not proposed_parent_id:
            return True

        proposed_parent = BimaErpCategory.objects.get_object_by_public_id(proposed_parent_id)

        if not proposed_parent or not proposed_parent.category:
            return True

        def is_descendant(category):
            for child in category.category_children.all():
                if child.public_id.hex == proposed_parent_id or is_descendant(child):
                    return True
            return False

        if is_descendant(category_to_edit):
            raise ValidationError({"error":_("A category cannot have its descendant as its parent.")})

    def perform_update(self, serializer):
        self.validate_category(self.request.data)
        serializer.save()

    def get_object(self):
        obj = BimaErpCategory.objects.get_object_by_public_id(self.kwargs['pk'])
        # self.check_object_permissions(self.request, obj)
        return obj

    def list_tags(self, request, *args, **kwargs):
        category = BimaErpCategory.objects.get_object_by_public_id(self.kwargs['public_id'])
        entity_tags = get_entity_tags_for_parent_entity(category).order_by('order')
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags, many=True)
        return Response(serialized_entity_tags.data)

    def create_tag(self, request, *args, **kwargs):
        category = BimaErpCategory.objects.get_object_by_public_id(self.kwargs['public_id'])
        result = create_single_entity_tag(request.data, category)
        if isinstance(result, BimaCoreEntityTag):
            serializer = BimaCoreEntityTagSerializer(result)
            return Response({
                "id": result.public_id,
                "tag_name": result.tag.name,
                "order": result.order
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(result, status=result.get("status", status.HTTP_500_INTERNAL_SERVER_ERROR))

    def get_tag(self, request, *args, **kwargs):
        category = BimaErpCategory.objects.get_object_by_public_id(self.kwargs['public_id'])
        entity_tags = get_object_or_404(BimaCoreEntityTag,
                                        public_id=self.kwargs['entity_tag_public_id'],
                                        parent_id=category.id)
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags)
        return JsonResponse(serialized_entity_tags.data)

    @action(detail=True)
    def all_parents(self, request, pk=None):
        category = self.get_object()
        parents = []
        parent = category.category
        while parent is not None:
            parents.append(BimaErpCategorySerializer(parent).data)
            parent = parent.category
        return Response(parents)

    @action(detail=True)
    def all_children(self, request, pk=None):
        category = self.get_object()
        children = []

        def get_children(category):
            if category.category_children.exists():
                for child in category.category_children.all():
                    children.append(BimaErpCategorySerializer(child).data)
                    get_children(child)

        get_children(category)
        return Response(children)

    @action(detail=True, methods=['GET'], url_path='direct_children')
    def direct_children(self, request, pk=None):
        category = self.get_object()
        direct_children = category.category_children.all()
        serializer = BimaErpCategorySerializer(direct_children, many=True)
        return Response(serializer.data)
