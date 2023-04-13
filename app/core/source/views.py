from core.abstract.views import AbstractViewSet
from core.source.models import BimaCoreSource
from core.source.serializers import BimaCoreSourceSerializer


class BimaCoreSourceViewSet(AbstractViewSet):
    queryset = BimaCoreSource.objects.all()
    serializer_class = BimaCoreSourceSerializer
    permission_classes = []
