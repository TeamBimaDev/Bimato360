from core.abstract.views import AbstractViewSet
from .models import BimaTreasuryPaymentProvider
from .serializers import BimaTreasuryPaymentProviderSerializer
from core.permissions import IsAdminOrReadOnly
from core.pagination import DefaultPagination
class BimaTreasuryPaymentProviderViewSet(AbstractViewSet):
    queryset = BimaTreasuryPaymentProvider.objects.all()
    serializer_class = BimaTreasuryPaymentProviderSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = DefaultPagination

    def get_object(self):
        obj = BimaTreasuryPaymentProvider.objects.get_object_by_public_id(self.kwargs['pk'])
        #self.check_object_permissions(self.request, obj)
        return obj