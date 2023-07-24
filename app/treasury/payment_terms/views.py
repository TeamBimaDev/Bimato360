from core.abstract.views import AbstractViewSet
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import BimaTreasuryPaymentTerms
from .serializers import BimaTreasuryPaymentTermsSerializer
from treasury.payment_terms_details.models import BimaTreasuryPaymentTermsDetails
from treasury.payment_terms_details.serializers import BimaTreasuryPaymentTermsDetailsSerializer


class BimaTreasuryPaymentTermsViewSet(AbstractViewSet):
    queryset = BimaTreasuryPaymentTerms.objects.all()
    serializer_class = BimaTreasuryPaymentTermsSerializer

    def get_object(self):
        obj = BimaTreasuryPaymentTerms.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=True, methods=['get'])
    def payment_terms_details(self, request, pk=None):
        payment_terms = self.get_object()

        payment_terms_details = BimaTreasuryPaymentTermsDetails.objects.filter(payment_terms=payment_terms)

        serializer = BimaTreasuryPaymentTermsDetailsSerializer(payment_terms_details, many=True)

        return Response(serializer.data)
