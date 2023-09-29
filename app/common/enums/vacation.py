from enum import Enum


class VacationType(Enum):
    ANNUAL = "Annual"
    SICK = "Sick"
    UNPAID = "Unpaid"
    OTHER = "Other"


class VacationStatus(Enum):
    PENDING = "Pending"
    APPROVED = "Approved"
    REFUSED = "Refused"


def get_vacation_type_list():
    return [(ff.value, ff.value) for ff in VacationType]


def get_vacation_status_list():
    return [(ff.value, ff.value) for ff in VacationStatus]
