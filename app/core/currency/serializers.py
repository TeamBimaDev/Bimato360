from core.abstract.serializers import AbstractSerializer
from core.currency.models import BimaCoreCurrency


class BimaCoreCurrencySerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreCurrency
        fields = [\
            'id', 'name', 'symbol', 'rounding', 'decimal_places', 'active', \
            'position', 'currency_unit_label', 'currency_subunit_label', \
            'created', 'updated' \
            ]
