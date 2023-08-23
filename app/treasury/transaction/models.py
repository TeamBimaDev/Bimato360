import logging

from common.enums.transaction_enum import TransactionNature
from common.enums.transaction_enum import get_transaction_nature_cash_or_bank, \
    get_transaction_direction_income_or_outcome
from core.abstract.models import AbstractModel
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from simple_history.models import HistoricalRecords
from treasury.bank_account.models import BimaTreasuryBankAccount
from treasury.cash.models import BimaTreasuryCash
from treasury.transaction_type.models import BimaTreasuryTransactionType

from .service import CashTransactionEffectStrategy, BankTransactionEffectStrategy, BimaTreasuryTransactionService

logger = logging.getLogger(__name__)


class BimaTreasuryTransaction(AbstractModel):
    nature = models.CharField(max_length=5, choices=get_transaction_nature_cash_or_bank(), verbose_name=_("Nature"))
    direction = models.CharField(max_length=7, choices=get_transaction_direction_income_or_outcome(),
                                 verbose_name=_("Direction"))
    transaction_type = models.ForeignKey(BimaTreasuryTransactionType, on_delete=models.PROTECT,
                                         verbose_name=_("Transaction Type"))
    cash = models.ForeignKey(BimaTreasuryCash, on_delete=models.PROTECT, null=True, blank=True, verbose_name=_("Cash"))
    bank_account = models.ForeignKey(BimaTreasuryBankAccount, on_delete=models.PROTECT, null=True, blank=True,
                                     verbose_name=_("Bank Account"))
    partner = models.ForeignKey(BimaErpPartner, on_delete=models.PROTECT, null=True, blank=True,
                                verbose_name=_("Partner"))
    note = models.TextField(null=True, blank=True, verbose_name=_("Notes"))
    date = models.DateField(verbose_name=_("Date"))
    expected_date = models.DateField(null=True, blank=True, verbose_name=_("Expected Date"))
    amount = models.DecimalField(max_digits=14, decimal_places=3, verbose_name=_("Amount"))
    reference = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Reference"))
    transaction_source = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                           verbose_name=_("Transaction Source"))
    partner_bank_account_number = models.CharField(max_length=32, verbose_name=_("Bank account number"), null=True,
                                                   blank=True)
    history = HistoricalRecords()

    def clean(self):
        if self.amount <= 0:
            logger.warning("Amount should be greater than 0")
            raise ValidationError(_('Amount should be greater than 0.'))

        if self.nature == TransactionNature.CASH.Name and not self.cash:
            logger.warning("Cash is required when nature is set to CASH.")
            raise ValidationError(_('Cash is required when nature is set to CASH.'))
        if self.nature == TransactionNature.BANK.Name and not self.bank_account:
            logger.warning("Bank Account is required when nature is set to BANK.")
            raise ValidationError(_('Bank Account is required when nature is set to BANK.'))

        if self.transaction_type.code in self.operation_bank_to_cash_or_inverse() and (
                not self.bank_account or not self.cash):
            logger.warning("Bank Account and Cash are required for FROM_ACCOUNT_TO_CASH transaction.")
            raise ValidationError(_('Bank Account and Cash are required for FROM_ACCOUNT_TO_CASH transaction.'))

        self.validate_transaction_type_and_nature_combination()

    def validate_transaction_type_and_nature_combination(self):
        error_message = None

        if (self.transaction_type.code == 'FROM_CASH_TO_ACCOUNT_INCOME' and
                self.transaction_type.income_outcome == 'INCOME' and
                self.direction == 'INCOME' and
                self.nature == TransactionNature.CASH.Name):
            error_message = _("You cannot do that. You should make this operation from Bank nature.")

        elif (self.transaction_type.code == 'FROM_ACCOUNT_TO_CASH_INCOME' and
              self.transaction_type.income_outcome == 'INCOME' and
              self.direction == 'INCOME' and
              self.nature == TransactionNature.BANK.Name):
            error_message = _("You cannot do that. You should make this operation from Cash nature.")

        if error_message:
            logger.warning(f"Validation failed for transaction {self.pk}: {error_message}")
            raise ValidationError(error_message)

    def save(self, *args, **kwargs):
        if self.pk:
            old_transaction = BimaTreasuryTransaction.objects.get(pk=self.pk)
            self.revert_effect(old_transaction)

        self.apply_effect()

        super(BimaTreasuryTransaction, self).save(*args, **kwargs)
        self.handle_auto_transaction()

    def get_effect_strategy(self):
        strategies = {
            TransactionNature.CASH.Name: CashTransactionEffectStrategy(),
            TransactionNature.BANK.Name: BankTransactionEffectStrategy(),
        }
        return strategies.get(self.nature)

    def revert_effect(self, transaction):
        strategy = self.get_effect_strategy()
        strategy.revert(transaction)

    def apply_effect(self):
        strategy = self.get_effect_strategy()
        strategy.apply(self)

    def handle_auto_transaction(self):
        if self.transaction_type.code in ['FROM_CASH_TO_ACCOUNT_OUTCOME',
                                          'FROM_ACCOUNT_TO_CASH_OUTCOME'] \
                and self.direction == TransactionNature.OUTCOME.Name:
            BimaTreasuryTransactionService.create_auto_transaction(self)

    def operation_bank_to_cash_or_inverse(self):
        return ['FROM_CASH_TO_ACCOUNT_OUTCOME', 'FROM_ACCOUNT_TO_CASH_OUTCOME', 'FROM_CASH_TO_ACCOUNT_INCOME',
                'FROM_ACCOUNT_TO_CASH_INCOME']


@receiver(post_delete, sender=BimaTreasuryTransaction)
def update_balance_on_delete(sender, instance, **kwargs):
    instance.revert_effect(instance)
