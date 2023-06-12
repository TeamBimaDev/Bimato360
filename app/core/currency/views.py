from core.abstract.views import AbstractViewSet
from core.currency.models import BimaCoreCurrency
from core.currency.serializers import BimaCoreCurrencySerializer


class BimaCoreCurrencyViewSet(AbstractViewSet):
    queryset = BimaCoreCurrency.objects.all()
    serializer_class = BimaCoreCurrencySerializer
    permission_classes = []
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['symbol', 'name', 'active', 'currency_unit_label', 'currency_subunit_label']

    def get_object(self):
        obj = BimaCoreCurrency.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
