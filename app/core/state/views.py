from core.abstract.views import AbstractViewSet
from core.state.models import BimaCoreState
from core.permissions import IsAdminOrReadOnly
from core.state.serializers import BimaCoreStateSerializer


class BimaCoreStateViewSet(AbstractViewSet):
    queryset = BimaCoreState.objects.all()
    serializer_class = BimaCoreStateSerializer
    permission_classes = [IsAdminOrReadOnly]
