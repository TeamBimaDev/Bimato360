from core.abstract.serializers import AbstractSerializer
from erp.partner.models import BimaErpPartner
from erp.purchase_document.serializers import BimaErpPurchaseDocumentUnpaidSerializer
from erp.sale_document.serializers import BimaErpSaleDocumentUnpaidSerializer
from rest_framework import serializers
from treasury.bank_account.models import BimaTreasuryBankAccount
from treasury.cash.models import BimaTreasuryCash
from treasury.transaction_type.models import BimaTreasuryTransactionType

from .models import BimaTreasuryTransaction, TransactionSaleDocumentPayment, TransactionPurchaseDocumentPayment
from .service import BimaTreasuryTransactionService


class BimaTreasuryTransactionSerializer(AbstractSerializer):
    partner = serializers.SerializerMethodField(read_only=True)
    partner_public_id = serializers.SlugRelatedField(
        queryset=BimaErpPartner.objects.all(),
        slug_field="public_id",
        source="partner",
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True,
    )

    transaction_type = serializers.SerializerMethodField(read_only=True)
    transaction_type_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryTransactionType.objects.all(),
        slug_field="public_id",
        source="transaction_type",
        write_only=True,
        required=True,
    )

    cash = serializers.SerializerMethodField(read_only=True)
    cash_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryCash.objects.all(),
        slug_field="public_id",
        source="cash",
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True,
    )

    bank_account = serializers.SerializerMethodField(read_only=True)
    bank_account_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryBankAccount.objects.all(),
        slug_field="public_id",
        source="bank_account",
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True,
    )

    transaction_source = serializers.SerializerMethodField(read_only=True)
    transaction_source_public_id = serializers.SlugRelatedField(
        queryset=BimaTreasuryTransaction.objects.all(),
        slug_field="public_id",
        source="transaction_source",
        write_only=True,
        required=False,
        allow_null=True,
        allow_empty=True,
    )

    def get_partner(self, obj):
        if obj.partner:
            return {
                "id": obj.partner.public_id.hex,
                "partner_type": obj.partner.partner_type,
                "first_name": obj.partner.first_name,
                "last_name": obj.partner.last_name,
                "company_name": obj.partner.company_name,
            }
        return None  # or return {} if you want an empty dictionary instead

    def get_transaction_type(self, obj):
        return {
            "id": obj.transaction_type.public_id.hex,
            "name": obj.transaction_type.name,
        }

    def get_cash(self, obj):
        if obj.cash:
            return {
                "id": obj.cash.public_id.hex,
                "name": obj.cash.name,
            }
        return None

    def get_bank_account(self, obj):
        if obj.bank_account:
            return {
                "id": obj.bank_account.public_id.hex,
                "name": obj.bank_account.name,
                "bank": obj.bank_account.bank.name,
                "currency": obj.bank_account.currency.name,
                "symbol": obj.bank_account.currency.symbol,
            }
        return None

    def get_transaction_source(self, obj):
        if obj.transaction_source:
            return {
                "id": obj.transaction_source.public_id.hex,
                "direction": obj.transaction_source.direction,
                "transaction_type": obj.transaction_source.transaction_type.name,
                "amount": obj.transaction_source.amount,
            }
        return None

    class Meta:
        model = BimaTreasuryTransaction
        fields = [
            "id",
            "number",
            "nature",
            "direction",
            "transaction_type",
            "transaction_type_public_id",
            "cash",
            "cash_public_id",
            "bank_account",
            "bank_account_public_id",
            "partner",
            "partner_public_id",
            "partner_bank_account_number",
            "amount",
            "remaining_amount",
            "date",
            "expected_date",
            "note",
            "reference",
            "transaction_source",
            "transaction_source_public_id",
            "created",
            "updated",
        ]
        read_only_fields = ('remaining_amount',)


class TransactionHistorySerializer(serializers.ModelSerializer):
    changes = serializers.SerializerMethodField()
    changed_by = serializers.SerializerMethodField()

    class Meta:
        model = BimaTreasuryTransaction.history.model
        fields = ("id", "changes", "changed_by", "history_date")

    def get_changes(self, instance):
        changes = []
        if instance.prev_record:
            diffs = instance.diff_against(instance.prev_record)
            for change in diffs.changes:
                old_value = self.get_readable_value(change.field, change.old)
                new_value = self.get_readable_value(change.field, change.new)
                changes.append(
                    {"field": change.field, "old": old_value, "new": new_value}
                )
        return changes

    def get_readable_value(self, field, value):
        transaction_service = BimaTreasuryTransactionService(None)
        retrieve_method = transaction_service.FIELD_TO_METHOD_MAP.get(field)
        if retrieve_method:
            return retrieve_method(transaction_service, value)

        return value

    def get_changed_by(self, instance):
        return instance.history_user.name if instance.history_user else None


class TransactionSaleDocumentPaymentSerializer(serializers.ModelSerializer):
    sale_document = BimaErpSaleDocumentUnpaidSerializer()

    class Meta:
        model = TransactionSaleDocumentPayment
        fields = ['transaction', 'sale_document', 'amount_paid']


class TransactionPurchaseDocumentPaymentSerializer(serializers.ModelSerializer):
    purchase_document = BimaErpPurchaseDocumentUnpaidSerializer()

    class Meta:
        model = TransactionPurchaseDocumentPayment
        fields = ['transaction', 'purchase_document', 'amount_paid']
