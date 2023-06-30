from core.abstract.views import AbstractViewSet
from .models import BimaTreasuryTransactionPaymentMethodBankTransferDetail
from .serializers import BimaTreasuryTransactionPaymentMethodBankTransferDetailSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination
class BimaTreasuryTransactionPaymentMethodBankTransferDetailViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransactionPaymentMethodBankTransferDetail.objects.all()
    serializer_class = BimaTreasuryTransactionPaymentMethodBankTransferDetailSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaTreasuryTransactionPaymentMethodBankTransferDetail.objects.get_object_by_public_id(self.kwargs['pk'])
        #self.check_object_permissions(self.request, obj)
        return obj