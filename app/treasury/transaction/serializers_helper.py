from rest_framework import serializers

from .models import TransactionSaleDocumentPayment


class SimpleTransactionSaleDocumentPaymentSerializer(serializers.ModelSerializer):
    transaction_public_id = serializers.SlugRelatedField(
        source='transaction',
        slug_field='public_id',
        read_only=True
    )
    transaction_number = serializers.SlugRelatedField(
        source='transaction',
        slug_field='number',
        read_only=True
    )

    class Meta:
        model = TransactionSaleDocumentPayment
        fields = ['amount_paid', 'transaction_public_id', 'transaction_number']
