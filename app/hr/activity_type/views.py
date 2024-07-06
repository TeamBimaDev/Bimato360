import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db.models import Q

from .models import BimaHrActivityType
from .serializers import BimaHrActivityTypeSerializer


class BimaHrActivityTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')

    class Meta:
        model = BimaHrActivityType
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(description__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))


class BimaHrActivityTypeViewSet(AbstractViewSet):
    queryset = BimaHrActivityType.objects.all()
    serializer_class = BimaHrActivityTypeSerializer
    permission_classes = []
    permission_classes = (ActionBasedPermission,)
    filterset_class = BimaHrActivityTypeFilter
    action_permissions = {
        'list': ['activity_type.can_read'],
        'create': ['activity_type.can_create'],
        'retrieve': ['activity_type.can_read'],
        'update': ['activity_type.can_update'],
        'partial_update': ['activity_type.can_update'],
        'destroy': ['activity_type.can_delete'],
    }

    def get_object(self):
        obj = BimaHrActivityType.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
