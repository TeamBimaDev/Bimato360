from core.abstract.views import AbstractViewSet
from .models import BimaErpVat
from .serializers import BimaErpVatSerializer


class BimaErpVatViewSet(AbstractViewSet):
    queryset = BimaErpVat.objects.all()
    serializer_class = BimaErpVatSerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = []

    def get_object(self):
        obj = BimaErpVat.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
