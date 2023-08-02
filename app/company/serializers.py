from core.abstract.serializers import AbstractSerializer
from core.currency.models import BimaCoreCurrency
from rest_framework import serializers

from .models import BimaCompany


class BimaCompanySerializer(AbstractSerializer):
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
        model = BimaCompany
        fields = [
            'id', 'name', 'email', 'phone', 'mobile',
            'fax', 'website', 'currency', 'currency_public_id', 'language',
            'timezone', 'header_note', 'footer_note', 'creation_date',
            'siren', 'siret', 'date_registration', 'rcs_number', 'date_struck_off',
            'ape_text', 'ape_code', 'capital', 'created', 'updated', 'default_pdf_invoice_format',
            'default_font_family', 'show_template_header', 'show_template_footer', 'show_template_logo', 'default_color'
        ]
