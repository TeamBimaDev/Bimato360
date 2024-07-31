<<<<<<< HEAD
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .filter import BimaTreasuryTransactionTypeFilter
from .models import BimaTreasuryTransactionType
from .serializers import BimaTreasuryTransactionTypeSerializer


class BimaTreasuryTransactionTypeViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransactionType.objects.all()
    serializer_class = BimaTreasuryTransactionTypeSerializer
    permission_classes = (ActionBasedPermission,)
    filterset_class = BimaTreasuryTransactionTypeFilter

    action_permissions = {
        'list': ['transaction_type.can_read'],
        'create': ['transaction_type.can_create'],
        'retrieve': ['transaction_type.can_read'],
        'update': ['transaction_type.can_update'],
        'partial_update': ['transaction_type.can_update'],
        'destroy': ['transaction_type.can_delete'],
    }

    def get_object(self):
        obj = BimaTreasuryTransactionType.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
=======
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .filter import BimaTreasuryTransactionTypeFilter
from .models import BimaTreasuryTransactionType
from .serializers import BimaTreasuryTransactionTypeSerializer


class BimaTreasuryTransactionTypeViewSet(AbstractViewSet):
    queryset = BimaTreasuryTransactionType.objects.all()
    serializer_class = BimaTreasuryTransactionTypeSerializer
    permission_classes = (ActionBasedPermission,)
    filterset_class = BimaTreasuryTransactionTypeFilter

    action_permissions = {
        'list': ['transaction_type.can_read'],
        'create': ['transaction_type.can_create'],
        'retrieve': ['transaction_type.can_read'],
        'update': ['transaction_type.can_update'],
        'partial_update': ['transaction_type.can_update'],
        'destroy': ['transaction_type.can_delete'],
    }

    def get_object(self):
        obj = BimaTreasuryTransactionType.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
>>>>>>> origin/ma-branch
