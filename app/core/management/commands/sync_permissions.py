from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.models import GlobalPermission

from common.permissions.permission_list import PermissionsList


class Command(BaseCommand):
    help = 'Sync permissions defined in permissions.py with the database'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(GlobalPermission)

        # Reflect on the Permissions class and get all the permissions defined
        permissions_in_class = [attr for attr in dir(PermissionsList) if not callable(attr) and not attr.startswith("__")]

        # Loop through permissions and create them if not exist in DB
        for perm_attr in permissions_in_class:
            permission_codename = getattr(PermissionsList, perm_attr)
            # Only create if doesn't exist
            if not Permission.objects.filter(codename=permission_codename).exists():
                Permission.objects.create(content_type=content_type, codename=permission_codename,
                                          name=permission_codename)

        self.stdout.write(self.style.SUCCESS('Successfully synced permissions'))
