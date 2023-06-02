from core.abstract.views import AbstractViewSet
from core.entity_tag.models import BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from core.pagination import DefaultPagination
from django.db.models import prefetch_related_objects
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404

from core.tag.models import BimaCoreTag
from rest_framework.response import Response


class BimaCoreEntityTagViewSet(AbstractViewSet):
    queryset = BimaCoreEntityTag.objects.select_related('tag').all()
    serializer_class = BimaCoreEntityTagSerializer
    permission_classes = []
    pagination_class = DefaultPagination

    def update(self, request, *args, **kwargs):
        try:
            partial = kwargs.pop('partial', False)
            instance = self.get_object()
            data_to_save = request.data.copy()
            data_to_save = get_tag_from_request(data_to_save)
            serializer = self.get_serializer(instance,
                                             data=data_to_save, partial=partial)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)
            queryset = self.filter_queryset(self.get_queryset())
            if queryset._prefetch_related_lookups:
                instance._prefetched_objects_cache = {}
                prefetch_related_objects([instance], *queryset._prefetch_related_lookups)
            return Response(serializer.data)
        except ValidationError as e:
            return Response(str(e),
                            status=status.HTTP_400_BAD_REQUEST)
        except BimaCoreEntityTag.DoesNotExist:
            return Response('Item was not found',
                            status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response(str(e),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get_object(self):
        obj = BimaCoreEntityTag.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj


def get_tag_from_request(data):
    tag = get_object_or_404(BimaCoreTag, public_id=data['tag'])
    data['tag_id'] = tag.id
    return data
