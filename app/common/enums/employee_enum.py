
from enum import Enum

from django.utils.translation import gettext_lazy as _


class EmploymentType(Enum):
    PERMANENT = _('Permanent')
    TEMPORARY = _('Temporary')


class WorkModeType(Enum):
    ONSITE = _('Onsite')
    REMOTE = _('Remote')
    HYBRID = _('Hybrid')


class JobTimeType(Enum):
    FULL_TIME = _('Full-time')
    PART_TIME = _('Part-time')
    INTERN = _('Intern')


class EmployeeStatusType(Enum):
    ACTIVE = _('Active')
    TERMINATED = _('Terminated')


class MaritalStatusType(Enum):
    SINGLE = _('Single')
    MARRIED = _('Married')
    DIVORCED = _('Divorced')
    WIDOWED = _('Widowed')
    SEPARATED = _('Separated')


def get_employment_type_choices():
    return [(emp_type.name, emp_type.value) for emp_type in EmploymentType]


def get_work_mode_choices():
    return [(wm.name, wm.value) for wm in WorkModeType]


def get_job_type_choices():
    return [(jt.name, jt.value) for jt in JobTimeType]


def get_employee_status_choices():
    return [(es.name, es.value) for es in EmployeeStatusType]


def get_marital_status_choices():
    return [(ms.name, ms.value) for ms in MaritalStatusType]

