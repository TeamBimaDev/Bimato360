from core.abstract.views import AbstractViewSet
from .models import BimaTreasuryPaymentTermsDetails
from .serializers import BimaTreasuryPaymentTermsDetailsSerializer


class BimaTreasuryPaymentTermsDetailsViewSet(AbstractViewSet):
    queryset = BimaTreasuryPaymentTermsDetails.objects.all()
    serializer_class = BimaTreasuryPaymentTermsDetailsSerializer

    def get_object(self):
        obj = BimaTreasuryPaymentTermsDetails.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
