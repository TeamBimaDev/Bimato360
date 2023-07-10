from datetime import timedelta
from uuid import UUID
from django.db.models import Q
import django_filters
from common.enums.sale_document_enum import SaleDocumentValidity

from django.utils import timezone

from .models import BimaErpSaleDocument


class SaleDocumentFilter(django_filters.FilterSet):
    number = django_filters.CharFilter(field_name='number', lookup_expr='icontains')
    status = django_filters.CharFilter(field_name='status', lookup_expr='iexact')
    type = django_filters.CharFilter(field_name='type', lookup_expr='iexact')
    partner = django_filters.CharFilter(method='filter_partner_hex')
    date_gte = django_filters.DateFilter(field_name='date', lookup_expr='gte')
    date_lte = django_filters.DateFilter(field_name='date', lookup_expr='lte')
    total_amount_gte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='gte')
    total_amount_lte = django_filters.NumberFilter(field_name='total_amount', lookup_expr='lte')
    validity_expired = django_filters.CharFilter(method='filter_validity_expired')
    product = django_filters.CharFilter(method='filter_product_hex')

    class Meta:
        model = BimaErpSaleDocument
        fields = ['number', 'status', 'type', 'partner', 'date_gte', 'date_lte', 'total_amount_gte', 'total_amount_lte',
                  'validity_expired']

    def filter_validity_expired(self, queryset, name, value):
        current_date = timezone.now().date()
        validity_days = {validity.name: int(validity.name.split("_")[1]) for validity in SaleDocumentValidity}

        if value == "ALL" or value is None:
            return queryset

        queries = Q()
        for validity, days in validity_days.items():
            if value == "EXPIRED":
                queries |= Q(date__lte=current_date - timedelta(days=days), validity=validity)
            elif value == "NOT_EXPIRED":
                queries |= Q(date__gt=current_date - timedelta(days=days), validity=validity)

        return queryset.filter(queries)

    def filter_partner_hex(self, queryset, name, value):
        try:
            uuid_value = UUID(hex=value)
            return queryset.filter(partner__public_id=uuid_value)
        except ValueError:
            return queryset

    def filter_product_hex(self, queryset, name, value):
        try:
            product_public_id = UUID(hex=value)
            return queryset.filter(bimaerpsaledocumentproduct__product__public_id=product_public_id)
        except ValueError:
            return queryset