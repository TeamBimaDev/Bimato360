

import django_filters
from common.converters.default_converters import str_to_bool
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db.models import Q

from .models import BimaCoreNotificationType
from .serializers import BimaCoreNotificationTypeSerializer


class BimaCoreNotificationTypeFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')

    class Meta:
        model = BimaCoreNotificationType
        fields = ['search', 'active']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))


class BimaCoreNotificationTypeViewSet(AbstractViewSet):
    queryset = BimaCoreNotificationType.objects.all()
    serializer_class = BimaCoreNotificationTypeSerializer
    filterset_class = BimaCoreNotificationTypeFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)

    action_permissions = {
        'list': ['notification_type.can_read'],
        'create': ['notification_type.can_create'],
        'retrieve': ['notification_type.can_read'],
        'update': ['notification_type.can_update'],
        'partial_update': ['notification_type.can_update'],
        'destroy': ['notification_type.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreNotificationType.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj


