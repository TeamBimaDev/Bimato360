from core.abstract.views import AbstractViewSet
from core.tags.models import BimaCoreTags
from core.tags.serializers import BimaCoreTagsserializer


class BimaCoreTagsViewSet(AbstractViewSet):
    queryset = BimaCoreTags.objects.all()
    serializer_class = BimaCoreTagsserializer
    permission_classes = []
