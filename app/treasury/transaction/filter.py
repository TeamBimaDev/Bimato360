import django_filters
from common.enums.transaction_enum import TransactionNature, TransactionDirection
from django.db import models

from .models import BimaTreasuryTransaction


class BimaTreasuryTransactionFilter(django_filters.FilterSet):
    nature = django_filters.CharFilter(method="filter_nature")
    direction = django_filters.CharFilter(method="filter_direction")
    transaction_type = django_filters.UUIDFilter(
        field_name="transaction_type__public_id"
    )
    payment_method = django_filters.UUIDFilter(
        field_name="payment_method__public_id"
    )
    cash = django_filters.UUIDFilter(field_name="cash__public_id")
    bank_account = django_filters.UUIDFilter(field_name="bank_account__public_id")
    partner = django_filters.UUIDFilter(field_name="partner__public_id")
    date_from = django_filters.DateFilter(field_name="date", lookup_expr="gte")
    date_to = django_filters.DateFilter(field_name="date", lookup_expr="lte")
    search = django_filters.CharFilter(method="filter_search")
    year = django_filters.NumberFilter(field_name="date", lookup_expr="year")

    class Meta:
        model = BimaTreasuryTransaction
        fields = []

    def filter_nature(self, queryset, name, value):
        if not TransactionNature.has_value(value):
            return queryset
        nature_value = TransactionNature.get_name(value).upper()
        return queryset.filter(nature=nature_value)

    def filter_direction(self, queryset, name, value):
        if not TransactionDirection.has_value(value):
            return queryset
        direction_value = TransactionDirection.get_name(value).upper()
        return queryset.filter(direction=direction_value)

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            models.Q(note__icontains=value)
            | models.Q(reference__icontains=value)
            | models.Q(partner_bank_account_number__icontains=value)
        )
