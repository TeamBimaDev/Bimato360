import django_filters
from common.enums.activity_status import get_presence_status_choices
from django_filters import rest_framework as filters

from .models import BimaHrActivity


class BimaHrActivityFilter(filters.FilterSet):
    person = django_filters.UUIDFilter(field_name='participants__person__public_id')
    presence_status = django_filters.ChoiceFilter(choices=get_presence_status_choices())
    start_date = django_filters.DateFromToRangeFilter(field_name='start_date')
    end_date = django_filters.DateFromToRangeFilter(field_name='end_date')
    activity_type = django_filters.UUIDFilter(field_name='activity_type__public_id')

    class Meta:
        model = BimaHrActivity
        fields = []
