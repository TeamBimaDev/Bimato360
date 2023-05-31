from core.abstract.views import AbstractViewSet
from core.currency.models import BimaCoreCurrency
from core.permissions import IsAdminOrReadOnly
from core.currency.serializers import BimaCoreCurrencySerializer
from core.pagination import DefaultPagination


class BimaCoreCurrencyViewSet(AbstractViewSet):
    queryset = BimaCoreCurrency.objects.all()
    serializer_class = BimaCoreCurrencySerializer
    permission_classes = []
    pagination_class = DefaultPagination
    def get_object(self):
        obj = BimaCoreCurrency.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj