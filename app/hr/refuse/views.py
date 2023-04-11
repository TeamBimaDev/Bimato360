from core.abstract.views import AbstractViewSet
from .serializers import  BimaHrRefuseSerializer
from .models import BimaHrRefuse

class BimaHrRefuseViewSet(AbstractViewSet):
    queryset = BimaHrRefuse.objects.all()
    serializer_class = BimaHrRefuseSerializer
    permission_classes = []






