from core.abstract.views import AbstractViewSet
from .models import BimaCorePoste
from .serializers import BimaCorePostESerializer

class BimaCorePosteViewSet(AbstractViewSet):
    queryset =BimaCorePoste.objects.all()
    serializer_class = BimaCorePostESerializer
    permission_classes = []