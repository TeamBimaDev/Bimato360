from enum import Enum

from django.utils.translation import gettext_lazy as _


class BimaHrInterviewStatus(Enum):
    PASSED = _('Passed')
    FAILED = _('Failed')
    REFUSED = _('Refused')
    PENDING = _('Pending')
    IN_PROGRESS = _('In Progress')


class BimaHrInterviewType(Enum):
    TECHNICAL = _('Technical')
    HR = _('Hr')
    INITIAL = _('Initial')


def get_interview_status_choices():
    return [(its.name, its.value) for its in BimaHrInterviewStatus]


def get_interview_type_choices():
    return [(cp.name, cp.value) for cp in BimaHrInterviewType]
