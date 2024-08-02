<<<<<<< HEAD
from core.abstract.views import AbstractViewSet
from core.pagination import DefaultPagination
from core.permissions import IsAdminOrReadOnly

from .models import BimaTreasuryRefund
from .serializers import BimaTreasuryRefundSerializer


class BimaTreasuryRefundViewSet(AbstractViewSet):
    queryset = BimaTreasuryRefund.objects.all()
    serializer_class = BimaTreasuryRefundSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    ordering = ["-date"]

    def get_object(self):
        obj = BimaTreasuryRefund.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
=======
from core.abstract.views import AbstractViewSet
from core.pagination import DefaultPagination
from core.permissions import IsAdminOrReadOnly

from .models import BimaTreasuryRefund
from .serializers import BimaTreasuryRefundSerializer


class BimaTreasuryRefundViewSet(AbstractViewSet):
    queryset = BimaTreasuryRefund.objects.all()
    serializer_class = BimaTreasuryRefundSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination
    ordering = ["-date"]

    def get_object(self):
        obj = BimaTreasuryRefund.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
>>>>>>> origin/ma-branch
