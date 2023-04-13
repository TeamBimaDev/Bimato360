from core.abstract.views import AbstractViewSet
from core.currency.models import BimaCoreCurrency
from core.permissions import IsAdminOrReadOnly
from core.currency.serializers import BimaCoreCurrencySerializer


class BimaCoreCurrencyViewSet(AbstractViewSet):
    queryset = BimaCoreCurrency.objects.all()
    serializer_class = BimaCoreCurrencySerializer
    permission_classes = []
