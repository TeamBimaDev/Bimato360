from core.abstract.views import AbstractViewSet
from core.tag.models import BimaCoreTag
from core.tag.serializers import BimaCoreTagSerializer
from core.pagination import DefaultPagination


class BimaCoreTagViewSet(AbstractViewSet):
    queryset = BimaCoreTag.objects.all()
    serializer_class = BimaCoreTagSerializer
    permission_classes = []
    pagination_class = DefaultPagination
    def get_object(self):
        obj = BimaCoreTag.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
