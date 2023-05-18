from core.abstract.views import AbstractViewSet
from .models import BimaCoreDepartment
from .serializers import BimaCoreDepartmentSerializer
class BimaCoreDepartmentViewSet(AbstractViewSet):
    queryset = BimaCoreDepartment.objects.all()
    serializer_class = BimaCoreDepartmentSerializer
    permission_classes = []
    def get_object(self):
        obj = BimaCoreDepartment.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj