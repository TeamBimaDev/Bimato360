from rest_framework import serializers
from .models import BimaTreasuryTransactionPaymentMethodChequeDetail
from core.abstract.serializers import AbstractSerializer
from treasury.transaction_payment_method.models import BimaTreasuryTransactionPaymentMethod


class BimaTreasuryTransactionPaymentMethodChequeDetailSerializer(AbstractSerializer):
    transaction_payment_method = serializers.SerializerMethodField(read_only=True)
    transaction_payment_method_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryTransactionPaymentMethod.objects.all(),
        slug_field='public_id',
        source='transaction_payment_method',
        write_only=True,
        required=False
    )

    def get_transaction_payment_method(self, obj):
        return {
            'id': obj.transaction_payment_method.public_id.hex,
            'name': obj.transaction_payment_method.name,
        }

    class Meta:
        model = BimaTreasuryTransactionPaymentMethodChequeDetail
        fields = [
            'id', 'bank_name', 'cheque_number', 'issue_date', 'account_number',
            'transaction_payment_method', 'transaction_payment_method_public_id', 'created', 'updated'
        ]
