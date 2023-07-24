from core.abstract.views import AbstractViewSet
from .models import BimaTreasuryTransactionPaymentMethodChequeDetail
from .serializers import BimaTreasuryTransactionPaymentMethodChequeDetailSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination
class BimaTreasuryTransactionPaymentMethodChequeDetailViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransactionPaymentMethodChequeDetail.objects.all()
    serializer_class = BimaTreasuryTransactionPaymentMethodChequeDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaTreasuryTransactionPaymentMethodChequeDetail.objects.get_object_by_public_id(self.kwargs['pk'])
        #self.check_object_permissions(self.request, obj)
        return obj