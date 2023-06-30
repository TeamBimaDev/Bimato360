from core.abstract.views import AbstractViewSet
from .models import BimaTreasuryRefund
from .serializers import BimaTreasuryRefundSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination


class BimaTreasuryRefundViewSet(AbstractViewSet):
    queryset = BimaTreasuryRefund.objects.all()
    serializer_class = BimaTreasuryRefundSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaTreasuryRefund.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
