from rest_framework import serializers
from .models import BimaTreasuryPaymentTermsDetails
from core.abstract.serializers import AbstractSerializer
from treasury.payment_terms.models import BimaTreasuryPaymentTerms


class BimaTreasuryPaymentTermsDetailsSerializer(AbstractSerializer):
    payment_terms = serializers.SerializerMethodField(read_only=True)
    payment_terms_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryPaymentTerms.objects.all(),
        slug_field='public_id',
        source='payment_terms',
        write_only=True,
        required=False
    )

    def get_payment_terms(self, obj):
        return {
            'id': obj.payment_terms.public_id.hex,
            'name': obj.payment_terms.name,
        }

    class Meta:
        model = BimaTreasuryPaymentTermsDetails
        fields = [
            'id', 'name', 'value', 'payment_terms', 'payment_terms_public_id', 'created', 'updated'
        ]
