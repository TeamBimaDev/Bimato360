from core.abstract.serializers import AbstractSerializer
from core.country.models import BimaCoreCountry

from core.currency.serializers import BimaCoreCurrencySerializer
from rest_framework import serializers

from core.currency.models import BimaCoreCurrency


class BimaCoreCountrySerializer(AbstractSerializer):
    currency = BimaCoreCurrencySerializer(read_only=True)  # Show currency details in list view
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreCurrency.objects.all(),
        source='currency',
        write_only=True  # Accept currency ID in edit view
    )

    class Meta:
        model = BimaCoreCountry
        fields = [
            'id', 'name', 'code', 'address_format', 'address_view_id', 'phone_code',
            'name_position', 'vat_label', 'state_required', 'zip_required', 'currency',
            'currency_id', 'created', 'updated'
        ]
