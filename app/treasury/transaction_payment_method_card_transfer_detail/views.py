from core.abstract.views import AbstractViewSet
from .models import BimaTreasuryTransactionPaymentMethodCardTransferDetail
from .serializers import BimaTreasuryTransactionPaymentMethodCardTransferDetailSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination
class BimaTreasuryTransactionPaymentMethodCardTransferDetailViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransactionPaymentMethodCardTransferDetail.objects.all()
    serializer_class = BimaTreasuryTransactionPaymentMethodCardTransferDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaTreasuryTransactionPaymentMethodCardTransferDetail.objects.get_object_by_public_id(self.kwargs['pk'])
        #self.check_object_permissions(self.request, obj)
        return obj