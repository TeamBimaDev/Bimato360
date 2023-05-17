from core.abstract.views import AbstractViewSet
from core.country.models import BimaCoreCountry
from core.permissions import IsAdminOrReadOnly
from core.country.serializers import BimaCoreCountrySerializer
from django.shortcuts import get_object_or_404

from core.currency.models import BimaCoreCurrency


class BimaCoreCountryViewSet(AbstractViewSet):
    queryset = BimaCoreCountry.objects.all()
    serializer_class = BimaCoreCountrySerializer
    permission_classes = []

    def create(self, request):
        print(f" test loool")
        currency_id = self.request.data.get('currency_id')
        currency = get_object_or_404(BimaCoreCurrency, id=currency_id)
        serializer.save(currency=currency)

    def update(self, request, pk=None):
        currency_public_id = self.request.data.get('currency')
        currency = get_object_or_404(BimaCoreCurrency, public_id=currency_public_id)
        request.data.currency = currency
        super().update(self,request)
    def get_object(self):
        obj = BimaCoreCountry.objects.get_object_by_public_id(self.kwargs['pk'])
        #self.check_object_permissions(self.request, obj)
        return obj