from enum import Enum
from django.utils.translation import gettext_lazy as _


class EntityStatus(Enum):
    ACTIVE = _('Active')
    INACTIVE = _('Inactive')
    BLOCKED = _('Blocked')


def get_entity_status_choices():
    return [(status.name, status.value) for status in EntityStatus]
