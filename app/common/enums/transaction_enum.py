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
