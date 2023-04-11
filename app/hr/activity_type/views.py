from core.abstract.views import AbstractViewSet

from .serializers import  BimaHrActivityTypeSerializer
from .models import BimaHrActivityType

class BimaHrActivityTypeViewSet(AbstractViewSet):
    queryset = BimaHrActivityType.objects.all()
    serializer_class = BimaHrActivityTypeSerializer
    permission_classes = []