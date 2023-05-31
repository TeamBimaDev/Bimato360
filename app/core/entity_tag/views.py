from core.abstract.views import AbstractViewSet
from core.entity_tag.models import BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer
from core.pagination import DefaultPagination


class BimaCoreEntityTagViewSet(AbstractViewSet):
    queryset = BimaCoreEntityTag.objects.all()
    serializer_class = BimaCoreEntityTagSerializer
    permission_classes = []
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaCoreEntityTag.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
