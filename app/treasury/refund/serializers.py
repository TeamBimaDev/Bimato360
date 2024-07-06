from rest_framework import serializers
from .models import BimaTreasuryRefund
from core.abstract.serializers import AbstractSerializer
from treasury.transaction.models import BimaTreasuryTransaction


class BimaTreasuryRefundSerializer(AbstractSerializer):
    transaction = serializers.SerializerMethodField(read_only=True)
    transaction_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryTransaction.objects.all(),
        slug_field='public_id',
        source='transaction',
        write_only=True,
        required=False
    )

    def get_transaction(self, obj):
        return {
            'id': obj.transaction.public_id.hex,
            'name': obj.transaction.name,
        }

    class Meta:
        model = BimaTreasuryRefund
        fields = [
            'id', 'amount', 'reason', 'date', 'transaction', 'transaction_public_id', 'created', 'updated'
        ]
