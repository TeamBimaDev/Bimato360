from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .models import BimaTreasuryPaymentMethod
from .serializers import BimaTreasuryPaymentMethodSerializer


class BimaTreasuryPaymentMethodViewSet(AbstractViewSet):
    queryset = BimaTreasuryPaymentMethod.objects.all()
    serializer_class = BimaTreasuryPaymentMethodSerializer
    permission_classes = (ActionBasedPermission,)
    filterset_class = BimaTreasuryPaymentMethod

    action_permissions = {
        'list': ['payment_method.can_read'],
        'create': ['payment_method.can_create'],
        'retrieve': ['payment_method.can_read'],
        'update': ['payment_method.can_update'],
        'partial_update': ['payment_method.can_update'],
        'destroy': ['payment_method.can_delete'],
    }

    def get_object(self):
        obj = BimaTreasuryPaymentMethod.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
