from core.abstract.views import AbstractViewSet
from .models import BimaErpUnitOfMeasure
from .serializers import BimaErpUnitOfMeasureSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination


class BimaErpUnitOfMeasureViewSet(AbstractViewSet):
    queryset = BimaErpUnitOfMeasure.objects.all()
    serializer_class = BimaErpUnitOfMeasureSerializer
    # permission_classes = [IsAdminOrReadOnly]
    permission_classes = []
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaErpUnitOfMeasure.objects.get_object_by_public_id(self.kwargs['pk'])
        # self.check_object_permissions(self.request, obj)
        return obj
