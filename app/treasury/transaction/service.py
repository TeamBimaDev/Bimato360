import logging

from common.enums.transaction_enum import TransactionNature
from treasury.transaction_type.models import BimaTreasuryTransactionType

logger = logging.getLogger(__name__)


def create_auto_transaction(transaction):
    from .models import BimaTreasuryTransaction

    complementary_transaction_mappings = {
        ('FROM_CASH_TO_ACCOUNT', 'OUTCOME'): ('FROM_CASH_TO_ACCOUNT', 'INCOME'),
        ('FROM_ACCOUNT_TO_CASH', 'OUTCOME'): ('FROM_ACCOUNT_TO_CASH', 'INCOME')
    }

    key = (transaction.transaction_type.code, transaction.direction)
    if key not in complementary_transaction_mappings:
        return  # If not, we don't create any automatic transaction

    complementary_code, complementary_direction = complementary_transaction_mappings[key]

    complementary_transaction_type = BimaTreasuryTransactionType.objects.get(
        code=complementary_code,
        income_outcome=complementary_direction
    )

    if transaction.nature == TransactionNature.CASH.Name:
        params = {
            "nature": 'BANK',
            "direction": 'INCOME',
            "transaction_type": complementary_transaction_type,
            "bank_account": transaction.bank_account,
            "date": transaction.date,
            "amount": transaction.amount,
            "transaction_source": transaction
        }
    elif transaction.nature == TransactionNature.BANK.Name:
        params = {
            "nature": 'CASH',
            "direction": 'INCOME',
            "transaction_type": complementary_transaction_type,
            "cash": transaction.cash,
            "date": transaction.date,
            "amount": transaction.amount,
            "transaction_source": transaction
        }

    created_transaction = BimaTreasuryTransaction.objects.create(**params)
    logger.info(f"Auto transaction {created_transaction.pk} created for transaction {transaction.pk}")
    return created_transaction


class TransactionEffectStrategy:
    def apply(self, transaction):
        raise NotImplementedError

    def revert(self, transaction):
        raise NotImplementedError


class CashTransactionEffectStrategy(TransactionEffectStrategy):
    def apply(self, transaction):
        transaction.cash.balance += transaction.amount \
            if transaction.direction == TransactionNature.INCOME.Name else -transaction.amount
        transaction.cash.save()

    def revert(self, transaction):
        transaction.cash.balance -= transaction.amount \
            if transaction.direction == TransactionNature.INCOME.Name else +transaction.amount
        transaction.cash.save()


class BankTransactionEffectStrategy(TransactionEffectStrategy):
    def apply(self, transaction):
        transaction.bank_account.balance += transaction.amount \
            if transaction.direction == TransactionNature.INCOME.Name else -transaction.amount
        transaction.bank_account.save()

    def revert(self, transaction):
        transaction.bank_account.balance -= transaction.amount \
            if transaction.direction == TransactionNature.INCOME.Name else +transaction.amount
        transaction.bank_account.save()
