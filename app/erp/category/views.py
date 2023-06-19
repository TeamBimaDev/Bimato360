from core.abstract.views import AbstractViewSet
from .models import BimaErpCategory
from .serializers import BimaErpCategorySerializer
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from core.entity_tag.models import get_entity_tags_for_parent_entity, create_single_entity_tag, BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from django.http import JsonResponse

class BimaErpCategoryViewSet(AbstractViewSet):
    queryset = BimaErpCategory.objects.all()
    serializer_class = BimaErpCategorySerializer
    permission_classes = []

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
                "tag_name": result.tag.name
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