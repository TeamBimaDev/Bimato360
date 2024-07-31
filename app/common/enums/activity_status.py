<<<<<<< HEAD
from enum import Enum

from django.utils.translation import gettext_lazy as _


class ActivityStatus(Enum):
    IN_PROGRESS = _('In Progress')
    CANCELED = _('Canceled')
    COMPLETED = _('Completed')


def get_activity_status_choices():
    return [(status.name, status.value) for status in ActivityStatus]


class PresenceStatus(Enum):
    CONFIRM = _('CONFIRM')
    CANCEL = _('CANCEL')
    MAYBE = _('MAYBE')
    NOT_SPECIFIED = _('Not Specified')


def get_presence_status_choices():
    return [(status.name, status.value) for status in PresenceStatus]
=======
from enum import Enum

from django.utils.translation import gettext_lazy as _


class ActivityStatus(Enum):
    IN_PROGRESS = _('In Progress')
    CANCELED = _('Canceled')
    COMPLETED = _('Completed')


def get_activity_status_choices():
    return [(status.name, status.value) for status in ActivityStatus]


class PresenceStatus(Enum):
    CONFIRM = _('CONFIRM')
    CANCEL = _('CANCEL')
    MAYBE = _('MAYBE')
    NOT_SPECIFIED = _('Not Specified')


def get_presence_status_choices():
    return [(status.name, status.value) for status in PresenceStatus]
>>>>>>> origin/ma-branch
