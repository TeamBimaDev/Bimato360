from core.abstract.views import AbstractViewSet
from core.currency.models import BimaCoreCurrency
from core.currency.serializers import BimaCoreCurrencySerializer


class BimaCoreCurrencyViewSet(AbstractViewSet):
    queryset = BimaCoreCurrency.objects.all()
    serializer_class = BimaCoreCurrencySerializer
    permission_classes = []

    def get_object(self):
        obj = BimaCoreCurrency.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
