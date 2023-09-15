import django_filters
from django.db.models import Q

from .models import BimaCoreNotification


class BimaCoreNotificationFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    notification_type = django_filters.UUIDFilter(field_name='notification_type__public_id')
    date_gte = django_filters.DateFilter(field_name='date_sent', lookup_expr='gte')
    date_lte = django_filters.DateFilter(field_name='date_sent', lookup_expr='lte')

    class Meta:
        model = BimaCoreNotification
        fields = ['search', 'notification_type', 'date_gte', 'date_lte']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(sender__icontains=value) |
            Q(subject__icontains=value) |
            Q(message__icontains=value)
        )
