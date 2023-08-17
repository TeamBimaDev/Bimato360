from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .models import BimaTreasuryPaymentTermDetail
from .serializers import BimaTreasuryPaymentTermDetailSerializer


class BimaTreasuryPaymentTermDetailViewSet(AbstractViewSet):
    queryset = BimaTreasuryPaymentTermDetail.objects.all()
    serializer_class = BimaTreasuryPaymentTermDetailSerializer
    permission_classes = (ActionBasedPermission,)

    action_permissions = {
        'list': ['payment_term.can_read'],
        'create': ['payment_term.can_create'],
        'retrieve': ['payment_term.can_read'],
        'update': ['payment_term.can_update'],
        'partial_update': ['payment_term.can_update'],
        'destroy': ['payment_term.can_delete'],
    }

    def get_object(self):
        obj = BimaTreasuryPaymentTermDetail.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
