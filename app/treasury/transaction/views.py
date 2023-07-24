from core.abstract.views import AbstractViewSet
from .models import BimaTreasuryTransaction
from .serializers import BimaTreasuryTransactionSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination
class BimaTreasuryTransactionViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransaction.objects.all()
    serializer_class = BimaTreasuryTransactionSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaTreasuryTransaction.objects.get_object_by_public_id(self.kwargs['pk'])
        #self.check_object_permissions(self.request, obj)
        return obj