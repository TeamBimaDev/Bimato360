from core.abstract.views import AbstractViewSet
from core.state.models import BimaCoreState
from core.state.serializers import BimaCoreStateSerializer


class BimaCoreStateViewSet(AbstractViewSet):
    queryset = BimaCoreState.objects.select_related('country').all()
    serializer_class = BimaCoreStateSerializer
    permission_classes = []

    def get_object(self):
        obj = BimaCoreState.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
