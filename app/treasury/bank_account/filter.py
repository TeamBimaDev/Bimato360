import django_filters
from common.converters.default_converters import str_to_bool
from django.db.models import Q

from .models import BimaTreasuryBankAccount


class BimaTreasuryBankAccountFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')

    class Meta:
        model = BimaTreasuryBankAccount
        fields = ['active', 'search']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value) |
            Q(account_number__icontains=value) |
            Q(iban__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))
