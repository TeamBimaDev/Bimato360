from rest_framework import serializers
from core.abstract.serializers import AbstractSerializer
from core.country.models import BimaCoreCountry
from core.currency.models import BimaCoreCurrency


class BimaCoreCountrySerializer(AbstractSerializer):
    currency = serializers.SerializerMethodField(read_only=True)
    currency_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCurrency.objects.all(),
        slug_field='public_id',
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
            'phone_code', 'vat_label', 'zip_required',
            'currency', 'currency_public_id', 'created', 'updated'
        ]
