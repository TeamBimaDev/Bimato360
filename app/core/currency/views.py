from core.abstract.views import AbstractViewSet
from core.currency.models import BimaCoreCurrency
from core.currency.serializers import BimaCoreCurrencySerializer
from common.permissions.action_base_permission import ActionBasedPermission


class BimaCoreCurrencyViewSet(AbstractViewSet):
    queryset = BimaCoreCurrency.objects.all()
    serializer_class = BimaCoreCurrencySerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    ordering_fields = AbstractViewSet.ordering_fields + \
                      ['symbol', 'name', 'active', 'currency_unit_label', 'currency_subunit_label']

    action_permissions = {
        'list': ['currency.can_read'],
        'create': ['currency.can_create'],
        'retrieve': ['currency.can_read'],
        'update': ['currency.can_update'],
        'partial_update': ['currency.can_update'],
        'destroy': ['currency.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreCurrency.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
