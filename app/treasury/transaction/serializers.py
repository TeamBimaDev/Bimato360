from rest_framework import serializers
from .models import BimaTreasuryTransaction
from core.abstract.serializers import AbstractSerializer
from erp.partner.models import BimaErpPartner


class BimaTreasuryTransactionSerializer(AbstractSerializer):
    partner = serializers.SerializerMethodField(read_only=True)
    partner_public_id = serializers.SlugRelatedField(
        queryset=BimaErpPartner.objects.all(),
        slug_field='public_id',
        source='partner',
        write_only=True,
        required=False
    )

    def get_partner(self, obj):
        return {
            'id': obj.partner.public_id.hex,
            'name': obj.partner.name,
        }

    class Meta:
        model = BimaTreasuryTransaction
        fields = [
            'id', 'name', 'transaction_payment_method', 'amount', 'date', 'due_date', 'note', 'partner',
            'partner_public_id', 'created', 'updated'
        ]
