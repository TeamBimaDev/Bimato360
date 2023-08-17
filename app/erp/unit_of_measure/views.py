import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet

from .models import BimaErpUnitOfMeasure
from .serializers import BimaErpUnitOfMeasureSerializer


class UnitOfMeasureFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    active = django_filters.CharFilter(method='filter_active')

    class Meta:
        model = BimaErpUnitOfMeasure
        fields = ['active', 'name']

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))


class BimaErpUnitOfMeasureViewSet(AbstractViewSet):
    queryset = BimaErpUnitOfMeasure.objects.all()
    serializer_class = BimaErpUnitOfMeasureSerializer
    filterset_class = UnitOfMeasureFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    action_permissions = {
        'list': ['unit_of_measure.can_read'],
        'create': ['unit_of_measure.can_create'],
        'retrieve': ['unit_of_measure.can_read'],
        'update': ['unit_of_measure.can_update'],
        'partial_update': ['unit_of_measure.can_update'],
        'destroy': ['unit_of_measure.can_delete'],
    }

    def get_object(self):
        obj = BimaErpUnitOfMeasure.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
