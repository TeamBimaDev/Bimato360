from core.abstract.serializers import AbstractSerializer
from erp.partner.models import BimaErpPartner
from rest_framework import serializers
from simple_history.models import HistoricalRecords
from treasury.bank_account.models import BimaTreasuryBankAccount
from treasury.cash.models import BimaTreasuryCash
from treasury.transaction_type.models import BimaTreasuryTransactionType

from .models import BimaTreasuryTransaction


class BimaTreasuryTransactionSerializer(AbstractSerializer):
    partner = serializers.SerializerMethodField(read_only=True)
    partner_public_id = serializers.SlugRelatedField(
        queryset=BimaErpPartner.objects.all(),
        slug_field='public_id',
        source='partner',
        write_only=True,
        required=False
    )

    transaction_type = serializers.SerializerMethodField(read_only=True)
    transaction_type_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryTransactionType.objects.all(),
        slug_field='public_id',
        source='transaction_type',
        write_only=True,
        required=True
    )

    cash = serializers.SerializerMethodField(read_only=True)
    cash_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryCash.objects.all(),
        slug_field='public_id',
        source='cash',
        write_only=True,
        required=False
    )

    bank_account = serializers.SerializerMethodField(read_only=True)
    bank_account_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryBankAccount.objects.all(),
        slug_field='public_id',
        source='bank_account',
        write_only=True,
        required=False
    )

    def get_partner(self, obj):
        return {
            'id': obj.partner.public_id.hex,
            'name': obj.partner.name,
        }

    def get_transaction_type(self, obj):
        return {
            'id': obj.transaction_type.public_id.hex,
            'name': obj.transaction_type.name,
        }

    def get_cash(self, obj):
        return {
            'id': obj.cash.public_id.hex,
            'name': obj.cash.name,
        }

    def get_bank_account(self, obj):
        return {
            'id': obj.bank_account.public_id.hex,
            'name': obj.bank_account.name,
        }

    class Meta:
        model = BimaTreasuryTransaction
        fields = [
            'id', 'name', 'transaction_payment_method', 'amount', 'date', 'due_date', 'note', 'partner',
            'partner_bank_account_number', 'partner_public_id', 'transaction_type', 'transaction_type_public_id',
            'cash', 'cash_public_id', 'bank_account', 'bank_account_id', 'created', 'updated'
        ]


class TransactionHistorySerializer(serializers.ModelSerializer):
    changes = serializers.SerializerMethodField()
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = HistoricalRecords
        fields = ('id', 'changes', 'changed_by', 'history_date')

    def get_changes(self, instance):
        changes = []
        if instance.prev_record:
            diffs = instance.diff_against(instance.prev_record)
            for change in diffs.changes:
                changes.append({
                    "field": change.field,
                    "old": change.old,
                    "new": change.new
                })
        return changes

    def get_changed_by(self, instance):
        return instance.history_user.name if instance.history_user else None
