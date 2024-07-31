<<<<<<< HEAD
from core.abstract.serializers import AbstractSerializer
from core.currency.models import BimaCoreCurrency


class BimaCoreCurrencySerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreCurrency
        fields = [
            'id', 'name', 'symbol', 'decimal_places', 'active',
            'currency_unit_label', 'currency_subunit_label',
            'created', 'updated'
            ]
=======
from core.abstract.serializers import AbstractSerializer
from core.currency.models import BimaCoreCurrency


class BimaCoreCurrencySerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreCurrency
        fields = [
            'id', 'name', 'symbol', 'decimal_places', 'active',
            'currency_unit_label', 'currency_subunit_label',
            'created', 'updated'
            ]
>>>>>>> origin/ma-branch
