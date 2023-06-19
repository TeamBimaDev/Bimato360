from enum import Enum


class SaleDocumentTypes(Enum):
    QUOTE = "Quote"
    ORDER = "ORDER"
    INVOICE = "Invoice"
    CREDIT_NOTE = "Credit note"


class SaleDocumentStatus(Enum):
    DRAFT = "Draft"
    CONFIRMED = "Confirmed"
    CANCELED = "CANCELED"


class SaleDocumentValidity(Enum):
    day_30 = "30 days"
    day_15 = "15 days"
    day_10 = "10 days"
    day_45 = "45 days"


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
