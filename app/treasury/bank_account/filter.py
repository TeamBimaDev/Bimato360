import django_filters
from common.converters.default_converters import str_to_bool
from company.models import BimaCompany
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q
from erp.partner.models import BimaErpPartner

from .models import BimaTreasuryBankAccount


class BimaTreasuryBankAccountFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search')
    active = django_filters.CharFilter(method='filter_active')
    type = django_filters.CharFilter(method='filter_type_and_public_id')
    public_id = django_filters.CharFilter(method='filter_type_and_public_id')

    class Meta:
        model = BimaTreasuryBankAccount
        fields = ['active', 'search', 'type', 'public_id']

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

    def filter_type_and_public_id(self, queryset, name, value):
        type_value = self.form.cleaned_data.get('type', None)
        public_id_value = self.form.cleaned_data.get('public_id', None)

        if type_value and public_id_value:
            if type_value.casefold() == "partner".casefold():
                parent_type = ContentType.objects.get_for_model(BimaErpPartner)
                partner = BimaErpPartner.objects.get_object_by_public_id(public_id_value)
                return queryset.filter(parent_type=parent_type, parent_id=partner.id)
            elif type_value.casefold() == "company".casefold():
                parent_type = ContentType.objects.get_for_model(BimaCompany)
                company = BimaCompany.objects.get_object_by_public_id(public_id_value)
                return queryset.filter(parent_type=parent_type, parent_id=company.id)
        return queryset
