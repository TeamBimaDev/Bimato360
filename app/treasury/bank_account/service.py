from core.bank.models import BimaCoreBank
from core.currency.models import BimaCoreCurrency
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.exceptions import ValidationError
from treasury.bank_account.models import BimaTreasuryBankAccount


class BimaTreasuryBankAccountService:

    @staticmethod
    def get_bank_accounts_for_parent_entity(parent):
        return BimaTreasuryBankAccount.objects.filter(
            parent_type=ContentType.objects.get_for_model(parent),
            parent_id=parent.id
        )

    @staticmethod
    def get_bank_account_by_public_id_and_parent(public_id, parent):
        try:
            return BimaTreasuryBankAccount.objects.get(
                public_id=public_id,
                parent_id=parent.id
            )
        except ObjectDoesNotExist:
            return None

    @staticmethod
    def create_bank_account(bank_account_data, parent):
        try:
            bank = BimaCoreBank.objects.get_object_by_public_id(bank_account_data.get('bank_public_id'))
            currency = BimaCoreCurrency.objects.get_object_by_public_id(bank_account_data.get('currency_public_id'))
            bank_account = BimaTreasuryBankAccount(
                **bank_account_data,
                bank=bank,
                currency=currency,
                parent_type=ContentType.objects.get_for_model(parent),
                parent_id=parent.id
            )

            bank_account.full_clean()
            bank_account.save()
            return bank_account

        except ValidationError as e:
            return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
        except Exception as e:
            return {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}
