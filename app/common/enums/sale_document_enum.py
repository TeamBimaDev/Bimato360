from enum import Enum
from django.utils.translation import gettext_lazy as _

class SaleDocumentTypes(Enum):
    QUOTE = _("Quote")
    ORDER = _("ORDER")
    INVOICE = _("Invoice")
    CREDIT_NOTE = _("Credit note")


class SaleDocumentStatus(Enum):
    DRAFT = _("Draft")
    CONFIRMED = _("Confirmed")
    CANCELED = _("CANCELED")

class SaleDocumentValidity(Enum):
    day_30 = _("30 days")
    day_15 = _("15 days")
    day_10 = _("10 days")
    day_45 = _("45 days")


class SaleDocumentRecurringInterval(Enum):
    EVERY_DAY = 1
    MONTHLY = 30
    THREE_MONTHLY = 90
    YEARLY = 365


def get_sale_document_recurring_interval():
    return [(member.value, member.name.lower().replace('_', ' ')) for member in SaleDocumentRecurringInterval]


def get_sale_document_types():
    return [(tp.name, tp.value) for tp in SaleDocumentTypes]


def get_sale_document_status():
    return [(st.name, st.value) for st in SaleDocumentStatus]


def get_sale_document_validity():
    return [(vd.name, vd.value) for vd in SaleDocumentValidity]
