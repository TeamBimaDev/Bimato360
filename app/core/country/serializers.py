from rest_framework import serializers
from core.abstract.serializers import AbstractSerializer
from core.country.models import BimaCoreCountry
from core.currency.models import BimaCoreCurrency


class BimaCoreCountrySerializer(AbstractSerializer):
    currency = serializers.SerializerMethodField(read_only=True)
    currency_id = serializers.PrimaryKeyRelatedField(
        queryset=BimaCoreCurrency.objects.all(),
        source='currency',
        write_only=True
    )

    def get_currency(self, obj):
        return {
            'id': obj.currency.public_id.hex,
            'name': obj.currency.name,
        }

    class Meta:
        model = BimaCoreCountry
        fields = [
            'id', 'name', 'code', 'address_format',
            'address_view_id', 'phone_code', 'name_position',
            'vat_label', 'state_required', 'zip_required',
            'currency', 'currency_id', 'created', 'updated'
        ]
