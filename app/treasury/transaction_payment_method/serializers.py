from rest_framework import serializers
from .models import BimaTreasuryTransactionPaymentMethod
from core.abstract.serializers import AbstractSerializer
from treasury.transaction.models import BimaTreasuryTransaction
from treasury.payment_provider.models import BimaTreasuryPaymentProvider
from core.bank.models import BimaCoreBank
from core.cash.models import BimaCoreCash


class BimaTreasuryTransactionPaymentMethodSerializer(AbstractSerializer):
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

    payment_method = serializers.SerializerMethodField(read_only=True)
    payment_method_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryTransactionPaymentMethod.objects.all(),
        slug_field='public_id',
        source='payment_method',
        write_only=True,
        required=False
    )

    def get_payment_method(self, obj):
        return {
            'id': obj.payment_method.public_id.hex,
            'name': obj.payment_method.name,
        }

    payment_provider = serializers.SerializerMethodField(read_only=True)
    payment_provider_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryPaymentProvider.objects.all(),
        slug_field='public_id',
        source='payment_provider',
        write_only=True,
        required=False
    )

    def get_payment_provider(self, obj):
        return {
            'id': obj.payment_provider.public_id.hex,
            'name': obj.payment_provider.name,
        }

    bank = serializers.SerializerMethodField(read_only=True)
    bank_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreBank.objects.all(),
        slug_field='public_id',
        source='bank',
        write_only=True,
        required=False
    )

    def get_bank(self, obj):
        return {
            'id': obj.bank.public_id.hex,
            'name': obj.bank.name,
        }

    cash = serializers.SerializerMethodField(read_only=True)
    cash_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCash.objects.all(),
        slug_field='public_id',
        source='cash',
        write_only=True,
        required=False
    )

    def get_cash(self, obj):
        return {
            'id': obj.cash.public_id.hex,
            'name': obj.cash.name,
        }

    class Meta:
        model = BimaTreasuryTransactionPaymentMethod
        fields = [
            'id', 'amount', 'reference', 'idempotency_token', 'is_captured', 'due_date', 'transaction',
            'transaction_public_id', 'payment_method', 'payment_method_public_id', 'payment_provider',
            'payment_provider_public_id', 'bank', 'bank_public_id', 'cash', 'cash_public_id', 'created', 'updated'
        ]
