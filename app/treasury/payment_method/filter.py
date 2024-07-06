import django_filters
from common.converters.default_converters import str_to_bool
from django.db.models import Q

from .models import BimaTreasuryPaymentMethod


class BimaTreasuryPaymentMethodFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')
    income_outcome = django_filters.CharFilter(method='filter_income_outcome')
    cash_bank = django_filters.CharFilter(method='filter_cash_bank')

    class Meta:
        model = BimaTreasuryPaymentMethod
        fields = ['active', 'search', 'income_outcome', 'cash_bank']

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(name__icontains=value)
        )

    def filter_active(self, queryset, name, value):
        if value == 'all' or value is None:
            return queryset
        else:
            return queryset.filter(active=str_to_bool(value))

    def filter_income_outcome(self, queryset, name, value):
        if value.lower() in ['income', 'outcome']:
            return queryset.filter(income_outcome=value.upper())

    def filter_cash_bank(self, queryset, name, value):
        if value.lower() in ['cash', 'bank']:
            return queryset.filter(cash_bank=value.upper())
