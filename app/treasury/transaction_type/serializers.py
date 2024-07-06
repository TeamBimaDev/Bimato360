from core.abstract.serializers import AbstractSerializer

from .models import BimaTreasuryTransactionType


class BimaTreasuryTransactionTypeSerializer(AbstractSerializer):
    class Meta:
        model = BimaTreasuryTransactionType
        fields = [
            'id', 'name', 'active', 'note', 'code', 'is_system', 'income_outcome', 'cash_bank', 'created', 'updated'
        ]
        read_only_fields = ('code', 'is_system',)
