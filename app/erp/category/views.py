from core.abstract.views import AbstractViewSet
from .models import BimaErpCategory
from .serializers import BimaErpCategorySerializer


class BimaErpCategoryViewSet(AbstractViewSet):
    queryset = BimaErpCategory.objects.all()
    serializer_class = BimaErpCategorySerializer
    permission_classes = []

    def get_object(self):
        obj = BimaErpCategory.objects.get_object_by_public_id(self.kwargs['pk'])
        # self.check_object_permissions(self.request, obj)
        return obj
