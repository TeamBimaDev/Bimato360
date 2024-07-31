<<<<<<< HEAD
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.models import GlobalPermission

from common.permissions.permission_list import PermissionsList


class Command(BaseCommand):
    help = 'Sync permissions defined in permissions.py with the database'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(GlobalPermission)

        permissions_in_class = [getattr(PermissionsList, attr) for attr in dir(PermissionsList) if
                                not callable(attr) and not attr.startswith("__")]

        for permission_tuple in permissions_in_class:
            permission_codename, permission_name, permission_group = permission_tuple

            if not Permission.objects.filter(codename=permission_codename).exists():
                permission = Permission.objects.create(content_type=content_type, codename=permission_codename,
                                                       name=permission_name)

        self.stdout.write(self.style.SUCCESS('Successfully synced permissions'))
=======
from django.core.management.base import BaseCommand
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from core.models import GlobalPermission

from common.permissions.permission_list import PermissionsList


class Command(BaseCommand):
    help = 'Sync permissions defined in permissions.py with the database'

    def handle(self, *args, **options):
        content_type = ContentType.objects.get_for_model(GlobalPermission)

        permissions_in_class = [getattr(PermissionsList, attr) for attr in dir(PermissionsList) if
                                not callable(attr) and not attr.startswith("__")]

        for permission_tuple in permissions_in_class:
            permission_codename, permission_name, permission_group = permission_tuple

            if not Permission.objects.filter(codename=permission_codename).exists():
                permission = Permission.objects.create(content_type=content_type, codename=permission_codename,
                                                       name=permission_name)

        self.stdout.write(self.style.SUCCESS('Successfully synced permissions'))
>>>>>>> origin/ma-branch
