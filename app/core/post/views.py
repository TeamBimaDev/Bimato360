from core.abstract.views import AbstractViewSet
from .models import BimaCorePost
from .serializers import BimaCorePostSerializer


class BimaCorePostViewSet(AbstractViewSet):
    queryset = BimaCorePost.objects.select_related('department').all()
    serializer_class = BimaCorePostSerializer
    permission_classes = []

    def get_object(self):
        obj = BimaCorePost.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
