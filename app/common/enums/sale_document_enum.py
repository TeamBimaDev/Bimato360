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
    DAILY = _('QUOTIDIEN')
    WEEKLY = _('HEBDOMADAIRE')
    MONTHLY = _('MENSUEL')
    QUARTERLY = _('TRIMESTRIEL')
    YEARLY = _('ANNUEL')
    CUSTOM = _('PERSONNALISE')


class SaleDocumentRecurringIntervalCustomUnit(Enum):
    DAY = _('JOUR')
    WEEK = _('SEMAINE')
    MONTH = _("MOIS")
    YEAR = _("ANNEE")


class SaleDocumentRecurringIntervalCustomUnit(Enum):
    UNDEFINED = _('INDEFINIE')
    END_AT = _('TERMINE LE')
    END_AFTER = _("TERMINE APRES")


def get_sale_document_recurring_cycle():
    return [(ri.name, ri.value) for ri in SaleDocumentRecurringInterval]


def get_sale_document_recurring_interval():
    return [(ri.name, ri.value) for ri in SaleDocumentRecurringInterval]


def get_sale_document_recurring_custom_unit():
    return [(ut.name, ut.value) for ut in SaleDocumentRecurringIntervalCustomUnit]


def get_sale_document_types():
    return [(tp.name, tp.value) for tp in SaleDocumentTypes]


def get_sale_document_status():
    return [(st.name, st.value) for st in SaleDocumentStatus]


def get_sale_document_validity():
    return [(vd.name, vd.value) for vd in SaleDocumentValidity]
