from enum import Enum

from django.utils.translation import gettext_lazy as _


class VacationType(Enum):
    ANNUAL = _("Annual")
    SICK = _("Sick")
    UNPAID = _("Unpaid")
    OTHER = _("Other")


class VacationStatus(Enum):
    PENDING = _("Pending")
    APPROVED = _("Approved")
    REFUSED = _("Refused")


def get_vacation_type_list():
    return [(ff.name, ff.value) for ff in VacationType]


def get_vacation_status_list():
    return [(ff.name, ff.value) for ff in VacationStatus]
