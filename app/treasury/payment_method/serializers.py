from core.abstract.serializers import AbstractSerializer

from .models import BimaTreasuryPaymentMethod


class BimaTreasuryPaymentMethodSerializer(AbstractSerializer):
    class Meta:
        model = BimaTreasuryPaymentMethod
        fields = [
            'id', 'name', 'active', 'note', 'code', 'is_system', 'income_outcome', 'cash_bank', 'created', 'updated'
        ]
        read_only_fields = ('code', 'is_system',)
