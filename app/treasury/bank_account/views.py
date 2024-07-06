from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .filter import BimaTreasuryBankAccountFilter
from .models import BimaTreasuryBankAccount
from .serializers import BimaTreasuryBankAccountSerializer


class BimaTreasuryBankAccountViewSet(AbstractViewSet):
    queryset = BimaTreasuryBankAccount.objects.all()
    serializer_class = BimaTreasuryBankAccountSerializer
    permission_classes = (ActionBasedPermission,)
    filterset_class = BimaTreasuryBankAccountFilter

    action_permissions = {
        'list': ['bank_account.can_read'],
        'create': ['bank_account.can_create'],
        'retrieve': ['bank_account.can_read'],
        'update': ['bank_account.can_update'],
        'partial_update': ['bank_account.can_update'],
        'destroy': ['bank_account.can_delete'],
    }

    def get_object(self):
        obj = BimaTreasuryBankAccount.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
