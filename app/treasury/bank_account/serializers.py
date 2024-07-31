<<<<<<< HEAD
from core.abstract.serializers import AbstractSerializer
from core.bank.models import BimaCoreBank
from core.currency.models import BimaCoreCurrency
from rest_framework import serializers

from .models import BimaTreasuryBankAccount


class BimaTreasuryBankAccountSerializer(AbstractSerializer):
    currency = serializers.SerializerMethodField(read_only=True)
    currency_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCurrency.objects.all(),
        slug_field='public_id',
        source='currency',
        write_only=True
    )

    bank = serializers.SerializerMethodField(read_only=True)
    bank_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreBank.objects.all(),
        slug_field='public_id',
        source="bank",
        write_only=True
    )

    def get_currency(self, obj):
        return {
            'id': obj.currency.public_id.hex,
            'name': obj.currency.name,
        }

    def get_bank(self, obj):
        return {
            'id': obj.bank.public_id.hex,
            'name': obj.bank.name,
        }

    class Meta:
        model = BimaTreasuryBankAccount
        fields = [
            'id', 'name', 'account_number', 'iban', 'balance', 'account_holder_name', 'note', 'active',
            'currency', 'currency_public_id', 'bank', 'bank_public_id', 'created', 'updated'
        ]
        read_only_fields = ('balance',)
=======
from core.abstract.serializers import AbstractSerializer
from core.bank.models import BimaCoreBank
from core.currency.models import BimaCoreCurrency
from rest_framework import serializers

from .models import BimaTreasuryBankAccount


class BimaTreasuryBankAccountSerializer(AbstractSerializer):
    currency = serializers.SerializerMethodField(read_only=True)
    currency_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreCurrency.objects.all(),
        slug_field='public_id',
        source='currency',
        write_only=True
    )

    bank = serializers.SerializerMethodField(read_only=True)
    bank_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreBank.objects.all(),
        slug_field='public_id',
        source="bank",
        write_only=True
    )

    def get_currency(self, obj):
        return {
            'id': obj.currency.public_id.hex,
            'name': obj.currency.name,
        }

    def get_bank(self, obj):
        return {
            'id': obj.bank.public_id.hex,
            'name': obj.bank.name,
        }

    class Meta:
        model = BimaTreasuryBankAccount
        fields = [
            'id', 'name', 'account_number', 'iban', 'balance', 'account_holder_name', 'note', 'active',
            'currency', 'currency_public_id', 'bank', 'bank_public_id', 'created', 'updated'
        ]
        read_only_fields = ('balance',)
>>>>>>> origin/ma-branch
