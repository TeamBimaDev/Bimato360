import logging
from datetime import datetime

from common.enums.transaction_enum import TransactionNature, TransactionDirection
from common.enums.transaction_enum import (
    get_transaction_nature_cash_or_bank,
    get_transaction_direction_income_or_outcome,
)
from core.abstract.models import AbstractModel
from django.core.exceptions import ValidationError
from django.db import models, transaction
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _
from erp.partner.models import BimaErpPartner
from simple_history.models import HistoricalRecords
from treasury.bank_account.models import BimaTreasuryBankAccount
from treasury.cash.models import BimaTreasuryCash
from treasury.payment_method.models import BimaTreasuryPaymentMethod
from treasury.transaction_type.models import BimaTreasuryTransactionType

from .service import (
    CashTransactionEffectStrategy,
    BankTransactionEffectStrategy,
    BimaTreasuryTransactionService,
)
from .service_payment_invoice import handle_invoice_payment_deletion, get_total_amount_used_for_transaction

logger = logging.getLogger(__name__)


class BimaTreasuryTransaction(AbstractModel):
    skip_child_validation = False
    skip_revert_apply_effect_validation = False
    number = models.CharField(
        max_length=32, null=False, blank=False, unique=True, verbose_name=_("Number")
    )
    nature = models.CharField(
        max_length=5,
        choices=get_transaction_nature_cash_or_bank(),
        verbose_name=_("Nature"),
    )
    direction = models.CharField(
        max_length=7,
        choices=get_transaction_direction_income_or_outcome(),
        verbose_name=_("Direction"),
    )
    transaction_type = models.ForeignKey(
        BimaTreasuryTransactionType,
        on_delete=models.PROTECT,
        verbose_name=_("Transaction Type"),
    )
    payment_method = models.ForeignKey(
        BimaTreasuryPaymentMethod,
        on_delete=models.PROTECT,
        verbose_name=_("Transaction Type"),
        null=True,
        blank=True
    )
    cash = models.ForeignKey(
        BimaTreasuryCash,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Cash"),
    )
    bank_account = models.ForeignKey(
        BimaTreasuryBankAccount,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Bank Account"),
    )
    partner = models.ForeignKey(
        BimaErpPartner,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        verbose_name=_("Partner"),
    )
    note = models.TextField(null=True, blank=True, verbose_name=_("Notes"))
    date = models.DateField(verbose_name=_("Date"))
    expected_date = models.DateField(
        null=True, blank=True, verbose_name=_("Expected Date")
    )
    amount = models.DecimalField(
        max_digits=14, decimal_places=3, verbose_name=_("Amount")
    )
    remaining_amount = models.DecimalField(
        max_digits=18,
        decimal_places=3,
        blank=True,
        null=True,
        default=0,
        verbose_name=_("Amount Paid"),
    )
    reference = models.CharField(
        max_length=64, null=True, blank=True, verbose_name=_("Reference")
    )
    transaction_source = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_("Transaction Source"),
    )
    partner_bank_account_number = models.CharField(
        max_length=32, verbose_name=_("Bank account number"), null=True, blank=True
    )
    history = HistoricalRecords()

    def clean(self):
        if self.amount <= 0:
            logger.warning("Amount should be greater than 0")
            raise ValidationError(_("Amount should be greater than 0."))

        if self.nature == TransactionNature.CASH.name and not self.cash:
            logger.warning("Cash is required when nature is set to CASH.")
            raise ValidationError(_("Cash is required when nature is set to CASH."))
        if self.nature == TransactionNature.BANK.name and not self.bank_account:
            logger.warning("Bank Account is required when nature is set to BANK.")
            raise ValidationError(
                _("Bank Account is required when nature is set to BANK.")
            )

        if self.transaction_type.code in self.operation_bank_to_cash_or_inverse() and (
                not self.bank_account or not self.cash
        ):
            logger.warning(
                "Bank Account and Cash are required for FROM_ACCOUNT_TO_CASH transaction."
            )
            raise ValidationError(
                _(
                    "Bank Account and Cash are required for FROM_ACCOUNT_TO_CASH transaction."
                )
            )
        # si création d'une transaction automaique donc il ne faut pas verifier
        if not self.transaction_source:
            self.validate_transaction_type_and_nature_combination()

        self.verify_expected_date()

    def verify_expected_date(self):
        if not self.expected_date or self.expected_date == "":
            self.expected_date = None
        else:
            try:
                datetime.strptime(str(self.expected_date), "%Y-%m-%d")
            except ValueError:
                self.expected_date = None

    def validate_transaction_type_and_nature_combination(self):
        error_message = None

        if (
                self.transaction_type.code == "FROM_CASH_TO_ACCOUNT_INCOME"
                and self.transaction_type.income_outcome == TransactionDirection.INCOME.name
                and self.direction == TransactionDirection.INCOME.name
                and self.nature == TransactionNature.BANK.name
        ):
            error_message = _(
                "You cannot do that. You should make this operation from Cash."
            )

        elif (
                self.transaction_type.code == "FROM_ACCOUNT_TO_CASH_INCOME"
                and self.transaction_type.income_outcome == TransactionDirection.INCOME.name
                and self.direction == TransactionDirection.INCOME.name
                and self.nature == TransactionNature.CASH.name
        ):
            error_message = _(
                "You cannot do that. You should make this operation from Bank."
            )

        if error_message:
            logger.warning(
                f"Validation failed for transaction {self.pk}: {error_message}"
            )
            raise ValidationError(error_message)

    def save(self, *args, **kwargs):
        self.clean()
        with transaction.atomic():
            if self.pk:
                old_transaction = BimaTreasuryTransaction.objects.get(pk=self.pk)
                self.check_if_transaction_child_and_prevent_modification(
                    old_transaction
                )
                if not self.__class__.skip_revert_apply_effect_validation:
                    revert_effect(old_transaction)
                self.remaining_amount = get_total_amount_used_for_transaction(self)

                super(BimaTreasuryTransaction, self).save(*args, **kwargs)

                if not self.__class__.skip_revert_apply_effect_validation:
                    self.refresh_from_db()
                    apply_effect(self)

                self.handle_auto_transaction(old_transaction)
            else:
                self.remaining_amount = self.amount
                super(BimaTreasuryTransaction, self).save(*args, **kwargs)
                if not self.__class__.skip_revert_apply_effect_validation:
                    self.refresh_from_db()
                    apply_effect(self)
                self.handle_auto_transaction()

    def delete(self, *args, **kwargs):
        system_delete = kwargs.pop("system_delete", False)
        self.check_if_transaction_child_and_prevent_deletion(system_delete)
        if self.has_payment():
            raise ValidationError(_("You cannot delete this transaction, you need to unlink invoice payment first"))
        handle_invoice_payment_deletion(self)
        super(BimaTreasuryTransaction, self).delete(*args, **kwargs)

    def has_payment(self):
        return self.transactionsaledocumentpayment_set.exists() or self.transactionpurchasedocumentpayment_set.exists()

    def handle_auto_transaction(self, old_transaction=None):
        if (
                self.transaction_type.code
                in ["FROM_CASH_TO_ACCOUNT_OUTCOME", "FROM_ACCOUNT_TO_CASH_OUTCOME"]
                and self.direction == TransactionDirection.OUTCOME.name
        ):
            child_transaction = BimaTreasuryTransaction.objects.filter(
                transaction_source=self
            ).first()

            if child_transaction:
                self.apply_change_on_transaction_child(
                    old_transaction, child_transaction
                )
            else:
                BimaTreasuryTransactionService.create_auto_transaction(self)

    def operation_bank_to_cash_or_inverse(self):
        return [
            "FROM_CASH_TO_ACCOUNT_OUTCOME",
            "FROM_ACCOUNT_TO_CASH_OUTCOME",
            "FROM_CASH_TO_ACCOUNT_INCOME",
            "FROM_ACCOUNT_TO_CASH_INCOME",
        ]

    def check_if_transaction_child_and_prevent_deletion(self, system_delete=False):
        if self.transaction_source and not system_delete:
            raise ValidationError(
                _(
                    "This transaction is created automatically from another one, it's not possible to delete it"
                )
            )

    def check_if_transaction_child_and_prevent_modification(self, old_transaction):
        if self.transaction_source and not self.__class__.skip_child_validation:
            changed_fields = [
                f.name
                for f in self._meta.fields
                if getattr(self, f.name) != getattr(old_transaction, f.name)
            ]
            if set(changed_fields) - {"note"}:
                raise ValidationError(
                    _(
                        "This transaction is created automatically form another one, it's not possible to edit it"
                    )
                )

    def apply_change_on_transaction_child(self, old_transaction, child_transaction):
        revert_effect(child_transaction)
        child_transaction.refresh_from_db()
        self.refresh_from_db()
        child_transaction.amount = self.amount
        child_transaction.date = self.date
        child_transaction.reference = self.reference
        child_transaction.cash = self.cash
        child_transaction.bank_account = self.bank_account

        self.__class__.skip_revert_apply_effect_validation = True
        self.__class__.skip_child_validation = True
        child_transaction.save()
        self.__class__.skip_revert_apply_effect_validation = False
        self.__class__.skip_child_validation = False

        apply_effect(child_transaction)


class TransactionSaleDocumentPayment(models.Model):
    transaction = models.ForeignKey(BimaTreasuryTransaction, on_delete=models.CASCADE)
    sale_document = models.ForeignKey('erp.BimaErpSaleDocument', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=3)

    class Meta:
        unique_together = ('transaction', 'sale_document')


class TransactionPurchaseDocumentPayment(models.Model):
    transaction = models.ForeignKey(BimaTreasuryTransaction, on_delete=models.CASCADE)
    purchase_document = models.ForeignKey('erp.BimaErpPurchaseDocument', on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=14, decimal_places=3)

    class Meta:
        unique_together = ('transaction', 'purchase_document')


def get_effect_strategy(transaction):
    strategies = {
        TransactionNature.CASH.name: CashTransactionEffectStrategy(),
        TransactionNature.BANK.name: BankTransactionEffectStrategy(),
    }
    return strategies.get(transaction.nature)


def revert_effect(transaction):
    strategy = get_effect_strategy(transaction)
    strategy.revert(transaction)


def apply_effect(transaction):
    strategy = get_effect_strategy(transaction)
    strategy.apply(transaction)


@receiver(pre_delete, sender=BimaTreasuryTransaction)
def update_balance_on_pre_delete(sender, instance, **kwargs):
    child_transaction = BimaTreasuryTransaction.objects.filter(
        transaction_source=instance
    ).first()
    if child_transaction:
        child_transaction.delete(system_delete=True)

    revert_effect(instance)
