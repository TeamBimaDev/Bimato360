from core.abstract.views import AbstractViewSet
from core.tags.models import BimaCoreTags
from core.tags.serializers import BimaCoreTagsserializer
from core.pagination import DefaultPagination


class BimaCoreTagsViewSet(AbstractViewSet):
    queryset = BimaCoreTags.objects.all()
    serializer_class = BimaCoreTagsserializer
    permission_classes = []
    pagination_class = DefaultPagination
    def get_object(self):
        obj = BimaCoreTags.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
