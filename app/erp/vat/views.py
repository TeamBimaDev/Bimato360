from core.abstract.views import AbstractViewSet
from .models import BimaErpVat
from .serializers import BimaErpVatSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination


class BimaErpVatViewSet(AbstractViewSet):
    queryset = BimaErpVat.objects.all()
    serializer_class = BimaErpVatSerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = []
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaErpVat.objects.get_object_by_public_id(self.kwargs['pk'])
        # self.check_object_permissions(self.request, obj)
        return obj
