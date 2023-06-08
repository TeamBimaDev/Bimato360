from core.abstract.views import AbstractViewSet
from core.entity_tag.models import BimaCoreEntityTag
from core.entity_tag.serializers import BimaCoreEntityTagSerializer


class BimaCoreEntityTagViewSet(AbstractViewSet):
    queryset = BimaCoreEntityTag.objects.select_related('tag').all()
    serializer_class = BimaCoreEntityTagSerializer
    permission_classes = []

    def get_object(self):
        obj = BimaCoreEntityTag.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
