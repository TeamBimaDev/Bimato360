from core.abstract.serializers import AbstractSerializer
from erp.partner.models import BimaErpPartner
from rest_framework import serializers
from simple_history.models import HistoricalRecords

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

    def get_partner(self, obj):
        return {
            'id': obj.partner.public_id.hex,
            'name': obj.partner.name,
        }

    class Meta:
        model = BimaTreasuryTransaction
        fields = [
            'id', 'name', 'transaction_payment_method', 'amount', 'date', 'due_date', 'note', 'partner',
            'partner_bank_account_number', 'partner_public_id', 'created', 'updated'
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
