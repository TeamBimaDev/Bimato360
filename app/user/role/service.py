<<<<<<< HEAD
import logging

from django.contrib.auth.models import Permission

logger = logging.getLogger(__name__)


def filter_passed_permission_return_only_available(permissions):
    if permissions:
        permissions = [int(permission_id) for permission_id in permissions]
        existing_permissions = Permission.objects.filter(pk__in=permissions)
        non_existing_permissions = set(permissions) - set(existing_permissions.values_list('pk', flat=True))
        if non_existing_permissions:
            logger.warning(f"When saving role permission those permissions were not found: {non_existing_permissions}")
        return list(existing_permissions)

    return []
=======
import logging

from django.contrib.auth.models import Permission

logger = logging.getLogger(__name__)


def filter_passed_permission_return_only_available(permissions):
    if permissions:
        permissions = [int(permission_id) for permission_id in permissions]
        existing_permissions = Permission.objects.filter(pk__in=permissions)
        non_existing_permissions = set(permissions) - set(existing_permissions.values_list('pk', flat=True))
        if non_existing_permissions:
            logger.warning(f"When saving role permission those permissions were not found: {non_existing_permissions}")
        return list(existing_permissions)

    return []
>>>>>>> origin/ma-branch
