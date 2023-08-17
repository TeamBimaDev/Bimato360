from core.abstract.serializers import AbstractSerializer
from rest_framework import serializers
from treasury.payment_term.models import BimaTreasuryPaymentTerm

from treasury.payment_term_detail.models import BimaTreasuryPaymentTermDetail


class BimaTreasuryPaymentTermDetailSerializer(AbstractSerializer):
    payment_term = serializers.SerializerMethodField(read_only=True)
    payment_term_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryPaymentTerm.objects.all(),
        slug_field='public_id',
        source='payment_term',
        write_only=True,
        required=False
    )

    def get_payment_term(self, obj):
        return {
            'id': obj.payment_term.public_id.hex,
            'name': obj.payment_term.name,
        }

    class Meta:
        model = BimaTreasuryPaymentTermDetail
        fields = [
            'id', 'name', 'value', 'payment_term', 'payment_term_public_id', 'created', 'updated'
        ]
