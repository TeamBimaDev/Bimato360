import django_filters
from common.permissions.action_base_permission import ActionBasedPermission
from core.abstract.views import AbstractViewSet
from django.db.models import Q

from .models import BimaCoreNotificationTemplate
from .serializers import BimaCoreNotificationTemplateSerializer


class BimaCoreNotificationTemplateFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    notification_type = django_filters.UUIDFilter(field_name='notification_type__public_id')

    class Meta:
        model = BimaCoreNotificationTemplate
        fields = ['search', 'notification_type']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(subject__icontains=value) |
            Q(message__icontains=value)
        )


class BimaCoreNotificationTemplateViewSet(AbstractViewSet):
    queryset = BimaCoreNotificationTemplate.objects.all()
    serializer_class = BimaCoreNotificationTemplateSerializer
    filterset_class = BimaCoreNotificationTemplateFilter
    permission_classes = []
    permission_classes = (ActionBasedPermission,)

    action_permissions = {
        'list': ['notification_template.can_read'],
        'create': ['notification_template.can_create'],
        'retrieve': ['notification_template.can_read'],
        'update': ['notification_template.can_update'],
        'partial_update': ['notification_template.can_update'],
        'destroy': ['notification_template.can_delete'],
    }

    def get_object(self):
        obj = BimaCoreNotificationTemplate.objects.get_object_by_public_id(self.kwargs['pk'])
        return obj
