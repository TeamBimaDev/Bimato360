from core.abstract.views import AbstractViewSet
from core.tag.models import BimaCoreTag
from core.tag.serializers import BimaCoreTagSerializer


class BimaCoreTagViewSet(AbstractViewSet):
    queryset = BimaCoreTag.objects.all()
    serializer_class = BimaCoreTagSerializer
    permission_classes = []

    def get_object(self):
        obj = BimaCoreTag.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
