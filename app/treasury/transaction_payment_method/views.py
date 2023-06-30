from core.abstract.views import AbstractViewSet
from .models import BimaTreasuryTransactionPaymentMethod
from .serializers import BimaTreasuryTransactionPaymentMethodSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination
class BimaTreasuryTransactionPaymentMethodViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransactionPaymentMethod.objects.all()
    serializer_class = BimaTreasuryTransactionPaymentMethodSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaTreasuryTransactionPaymentMethod.objects.get_object_by_public_id(self.kwargs['pk'])
        #self.check_object_permissions(self.request, obj)
        return obj