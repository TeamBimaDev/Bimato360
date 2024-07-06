import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db.models import Q

from .models import BimaErpVat
from .serializers import BimaErpVatSerializer


class VatFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')

    class Meta:
        model = BimaErpVat
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(rate__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))


class BimaErpVatViewSet(AbstractViewSet):
    queryset = BimaErpVat.objects.all()
    serializer_class = BimaErpVatSerializer
    filterset_class = VatFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['vat.can_read'],
        'create': ['vat.can_create'],
        'retrieve': ['vat.can_read'],
        'update': ['vat.can_update'],
        'partial_update': ['vat.can_update'],
        'destroy': ['vat.can_delete'],
    }

    def get_object(self):
        obj = BimaErpVat.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
