import django_filters
from common.enums.employee_enum import get_marital_status_choices
from django.db import models
from django_filters import rest_framework as filters

from .models import BimaHrEmployee


class BimaHrEmployeeFilter(filters.FilterSet):
    marital_status = django_filters.ChoiceFilter(choices=get_marital_status_choices())
    position = django_filters.UUIDFilter(field_name='position__public_id', lookup_expr='iexact')

    search = django_filters.CharFilter(
        method='filter_search',
        label='Search in first_name, last_name, email, phone number, and second phone number',
    )

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(first_name__icontains=value) |
            models.Q(last_name__icontains=value) |
            models.Q(email__icontains=value) |
            models.Q(phone_number__icontains=value) |
            models.Q(second_phone_number__icontains=value)
        )

    class Meta:
        model = BimaHrEmployee
        fields = []
