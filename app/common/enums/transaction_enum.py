from enum import Enum

from django.utils.translation import gettext_lazy as _


class TransactionType(Enum):
    INCOME = _("Income")
    EXPENSE = _("Expense")


def get_transaction_types():
    return [(tp.name, tp.value) for tp in TransactionType]


class PaymentTermDetailType(Enum):
    PERCENT = _('Percentage')
    FIXED = _('Fixed Amount')
    BALANCE = _("Balance")


def get_payment_term_detail_types():
    return [(ptd.name, ptd.value) for ptd in PaymentTermDetailType]


class TransactionTypeIncomeOutcome(Enum):
    INCOME = _('INCOME')
    OUTCOME = _('OUTCOME')


def get_transaction_type_income_outcome():
    return [(ptd.name, ptd.value) for ptd in TransactionTypeIncomeOutcome]


class TransactionTypeForCashOrBank(Enum):
    Cash = _('Cash')
    Bank = _('Bank')


def get_transaction_type_for_cash_or_bank():
    return [(ptd.name, ptd.value) for ptd in TransactionTypeForCashOrBank]


class TransactionNature(Enum):
    CASH = _('Cash')
    BANK = _('Bank')

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def get_name(cls, value):
        return next((item.name for item in cls if item.value == value), None)


def get_transaction_nature_cash_or_bank():
    return [(ptd.name, ptd.value) for ptd in TransactionNature]


class TransactionDirection(Enum):
    INCOME = _('Income')
    OUTCOME = _('Outcome')

    @classmethod
    def has_value(cls, value):
        return any(value == item.value for item in cls)

    @classmethod
    def get_name(cls, value):
        return next((item.name for item in cls if item.value == value), None)


def get_transaction_direction_income_or_outcome():
    return [(ptd.name, ptd.value) for ptd in TransactionDirection]
