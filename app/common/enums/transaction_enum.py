from enum import Enum

from django.utils.translation import gettext_lazy as _


class TransactionTypeIncomeOutcome(Enum):
    INCOME = _("INCOME")
    OUTCOME = _("OUTCOME")


def get_transaction_type_income_outcome():
    return [(ptd.name, ptd.value) for ptd in TransactionTypeIncomeOutcome]


class TransactionTypeForCashOrBank(Enum):
    CASH = _("Cash")
    BANK = _("Bank")


def get_transaction_type_for_cash_or_bank():
    return [(ptd.name, ptd.value) for ptd in TransactionTypeForCashOrBank]


class TransactionNature(Enum):
    CASH = _("Cash")
    BANK = _("Bank")

    @classmethod
    def has_value(cls, value):
        return any(value.lower() == item.name.lower() for item in cls)

    @classmethod
    def get_name(cls, value):
        return next(
            (item.name for item in cls if item.name.lower() == value.lower()), None
        )


def get_transaction_nature_cash_or_bank():
    return [(ptd.name, ptd.value) for ptd in TransactionNature]


class TransactionDirection(Enum):
    INCOME = _("Income")
    OUTCOME = _("Outcome")

    @classmethod
    def has_value(cls, value):
        return any(value.lower() == item.name.lower() for item in cls)

    @classmethod
    def get_name(cls, value):
        return next(
            (item.name for item in cls if item.name.lower() == value.lower()), None
        )


def get_transaction_direction_income_or_outcome():
    return [(ptd.name, ptd.value) for ptd in TransactionDirection]


class PaymentTermType(Enum):
    IMMEDIATE = _("IMMEDIATE")
    AFTER_ONE_WEEK = _("AFTER_ONE_WEEK")
    AFTER_TWO_WEEK = _("AFTER_TWO_WEEK")
    END_OF_MONTH = _("END_OF_MONTH")
    NEXT_MONTH = _("NEXT_MONTH")
    CUSTOM = _("CUSTOM")


def get_payment_term_type():
    return [(ptd.name, ptd.value) for ptd in PaymentTermType]


class PaymentTermCustomType(Enum):
    IMMEDIATE = _("IMMEDIATE")
    AFTER_ONE_WEEK = _("AFTER_ONE_WEEK")
    AFTER_TWO_WEEK = _("AFTER_TWO_WEEK")
    END_OF_MONTH = _("END_OF_MONTH")
    NEXT_MONTH = _("NEXT_MONTH")


def get_payment_term_custom_type():
    return [(ptd.name, ptd.value) for ptd in PaymentTermCustomType]
