from core.abstract.serializers import AbstractSerializer
from core.country.models import BimaCoreCountry

from core.currency.serializers import BimaCoreCurrencySerializer


class BimaCoreCountrySerializer(AbstractSerializer):
    currency = BimaCoreCurrencySerializer()
    class Meta:
        model = BimaCoreCountry
        fields = [\
            'id', 'name', 'code', 'address_format', 'address_view_id', 'phone_code', \
            'name_position', 'vat_label', 'state_required', 'zip_required', 'currency', \
            'created', 'updated' \
            ]
