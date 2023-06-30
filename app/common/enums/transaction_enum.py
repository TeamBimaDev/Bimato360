from enum import Enum
from django.utils.translation import gettext_lazy as _


class TransactionType(Enum):
    INCOME = _("Income")
    EXPENSE = _("Expense")


def get_transaction_types():
    return [(tp.name, tp.value) for tp in TransactionType]
