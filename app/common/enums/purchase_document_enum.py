from enum import Enum

from django.utils.translation import gettext_lazy as _


class PurchaseDocumentTypes(Enum):
    QUOTE = _("Quote")
    ORDER = _("ORDER")
    INVOICE = _("Invoice")
    CREDIT_NOTE = _("Credit note")
    RFQ = _("Request for Quotation")


class PurchaseDocumentStatus(Enum):
    DRAFT = _("Draft")
    CONFIRMED = _("Confirmed")
    CANCELED = _("CANCELED")


class PurchaseDocumentValidity(Enum):
    day_30 = _("30 days")
    day_15 = _("15 days")
    day_10 = _("10 days")
    day_45 = _("45 days")


class PurchaseDocumentRecurringInterval(Enum):
    EVERY_DAY = 1
    MONTHLY = 30
    THREE_MONTHLY = 90
    YEARLY = 365


class PurchaseDocumentPaymentStatus(Enum):
    NOT_PAID = _("NOT_PAD")
    PARTIAL_PAID = _("PARTIAL_PAID")
    PAID = _("PAID")


def get_purchase_document_recurring_interval():
    return [(member.value, member.name.lower().replace('_', ' ')) for member in PurchaseDocumentRecurringInterval]


def get_purchase_document_types():
    return [(tp.name, tp.value) for tp in PurchaseDocumentTypes]


def get_purchase_document_status():
    return [(st.name, st.value) for st in PurchaseDocumentStatus]


def get_purchase_document_validity():
    return [(vd.name, vd.value) for vd in PurchaseDocumentValidity]


def get_payment_status():
    return [(ps.name, ps.value) for ps in PurchaseDocumentPaymentStatus]
