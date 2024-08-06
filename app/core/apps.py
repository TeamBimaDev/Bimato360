

from django.apps import AppConfig
from django.core.management import call_command


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Call the management command to sync permissions when the app is ready
        call_command('sync_permissions')


