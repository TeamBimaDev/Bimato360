from django.utils.encoding import force_str
from rest_framework import serializers

from .models import TransactionSaleDocumentPayment, TransactionPurchaseDocumentPayment


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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        transaction = instance.transaction
        representation['transaction_public_id'] = force_str(transaction.public_id.hex)
        return representation

    class Meta:
        model = TransactionSaleDocumentPayment
        fields = ['amount_paid', 'transaction_public_id', 'transaction_number']


class SimpleTransactionPurchaseDocumentPaymentSerializer(serializers.ModelSerializer):
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

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        transaction = instance.transaction
        representation['transaction_public_id'] = force_str(transaction.public_id.hex)
        return representation

    class Meta:
        model = TransactionPurchaseDocumentPayment
        fields = ['amount_paid', 'transaction_public_id', 'transaction_number']
