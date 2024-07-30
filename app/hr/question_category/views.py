import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from core.entity_tag.models import get_entity_tags_for_parent_entity, create_single_entity_tag, BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaHrQuestionCategory
from .serializers import BimaHrQuestionCategorySerializer


class BimaHrQuestionCategoryFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')

    class Meta:
        model = BimaHrQuestionCategory
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))


class BimaHrQuestionCategoryViewSet(AbstractViewSet):
    queryset = BimaHrQuestionCategory.objects.all()
    serializer_class = BimaHrQuestionCategorySerializer
    filterset_class = BimaHrQuestionCategoryFilter
    permission_classes = []
    #permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['question_category.can_read'],
        'create': ['question_category.can_create'],
        'retrieve': ['question_category.can_read'],
        'update': ['question_category.can_update'],
        'partial_update': ['question_category.can_update'],
        'destroy': ['question_category.can_delete'],
    }
    
    def get_object(self):
        obj = BimaHrQuestionCategory.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    def list_tags(self, request, *args, **kwargs):
        category = BimaHrQuestionCategory.objects.get_object_by_public_id(self.kwargs['public_id'])
        entity_tags = get_entity_tags_for_parent_entity(category).order_by('order')
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags, many=True)
        return Response(serialized_entity_tags.data)

    def create_tag(self, request, *args, **kwargs):
        category = BimaHrQuestionCategory.objects.get_object_by_public_id(self.kwargs['public_id'])
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
        category = BimaHrQuestionCategory.objects.get_object_by_public_id(self.kwargs['public_id'])
        entity_tags = get_object_or_404(BimaCoreEntityTag,
                                        public_id=self.kwargs['entity_tag_public_id'],
                                        parent_id=category.id)
        serialized_entity_tags = BimaCoreEntityTagSerializer(entity_tags)
        return Response(serialized_entity_tags.data)

    @action(detail=True)
    def all_parents(self, request, pk=None):
        category = self.get_object()
        parents = []
        parent = category.category
        while parent is not None:
            parents.append(BimaHrQuestionCategorySerializer(parent).data)
            parent = parent.category
        return Response(parents)

    @action(detail=True)
    def all_children(self, request, pk=None):
        category = self.get_object()
        children = []

        def get_children(category):
            if category.category_children.exists():
                for child in category.category_children.all():
                    children.append(BimaHrQuestionCategorySerializer(child).data)
                    get_children(child)

        get_children(category)
        return Response(children)

    @action(detail=True, methods=['GET'], url_path='direct_children')
    def direct_children(self, request, pk=None):
        category = self.get_object()
        direct_children = category.category_children.all()
        serializer = BimaHrQuestionCategorySerializer(direct_children, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['GET'], url_path='all_parents_nested')
    def all_parents_nested(self, request, pk=None):
        category = self.get_object()

        def get_nested_parent(category):
            if category.category is None:
                return None
            else:
                parent_data = get_nested_parent(category.category)
                category_serializer_data = self.get_serializer(category.category).data
                if parent_data is not None:
                    category_serializer_data['category'] = parent_data
                return category_serializer_data

        nested_parents = get_nested_parent(category)
        return Response(nested_parents)

