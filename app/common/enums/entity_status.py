from enum import Enum


class EntityStatus(Enum):
    ACTIVE = 'Active'
    INACTIVE = 'Inactive'
    BLOCKED = 'Blocked'


def get_entity_status_choices():
    return [(status.name, status.value) for status in EntityStatus]
