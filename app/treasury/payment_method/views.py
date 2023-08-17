from core.abstract.views import AbstractViewSet
from core.pagination import DefaultPagination
from core.permissions import IsAdminOrReadOnly

from .models import BimaTreasuryPaymentMethod
from .serializers import BimaTreasuryPaymentMethodSerializer


class BimaTreasuryPaymentMethodViewSet(AbstractViewSet):
    queryset = BimaTreasuryPaymentMethod.objects.all()
    serializer_class = BimaTreasuryPaymentMethodSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaTreasuryPaymentMethod.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
