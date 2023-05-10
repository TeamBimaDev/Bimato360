from core.abstract.views import AbstractViewSet
from .models import BimaCorePost
from .serializers import BimaCorePostSerializer

class BimaCorePostViewSet(AbstractViewSet):
    queryset =BimaCorePost.objects.all()
    serializer_class = BimaCorePostSerializer
    permission_classes = []