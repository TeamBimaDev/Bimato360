from enum import Enum
from django.utils.translation import gettext_lazy as _


class ActivityStatus(Enum):
    IN_PROGRESS = _('In Progress')
    COMPLETED = _('Completed')


def get_activity_status_choices():
    return [(status.name, status.value) for status in ActivityStatus]