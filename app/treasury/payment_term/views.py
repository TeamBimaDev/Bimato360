from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from treasury.payment_term_detail.models import BimaTreasuryPaymentTermDetail
from treasury.payment_term_detail.serializers import BimaTreasuryPaymentTermDetailSerializer

from .filter import BimaTreasuryPaymentTermFilter
from .models import BimaTreasuryPaymentTerm
from .serializers import BimaTreasuryPaymentTermSerializer


class BimaTreasuryPaymentTermViewSet(AbstractViewSet):
    queryset = BimaTreasuryPaymentTerm.objects.all()
    serializer_class = BimaTreasuryPaymentTermSerializer
    permission_classes = (ActionBasedPermission,)
    filterset_class = BimaTreasuryPaymentTermFilter

    action_permissions = {
        'list': ['payment_term.can_read'],
        'create': ['payment_term.can_create'],
        'retrieve': ['payment_term.can_read'],
        'update': ['payment_term.can_update'],
        'partial_update': ['payment_term.can_update'],
        'destroy': ['payment_term.can_delete'],
    }

    def get_object(self):
        obj = BimaTreasuryPaymentTerm.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj

    @action(detail=True, methods=['get'])
    def payment_term_details(self, request, pk=None):
        payment_term = self.get_object()

        payment_term_details = BimaTreasuryPaymentTermDetail.objects.filter(payment_term=payment_term)

        serializer = BimaTreasuryPaymentTermDetailSerializer(payment_term_details, many=True)

        return Response(serializer.data)
