<<<<<<< HEAD
import os
import subprocess

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run all tests in all sub-apps of all apps.'

    def handle(self, *args, **options):
        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            app_name = app_config.name
            if app_name == 'simple_history':
                continue

            app_path = app_config.path
            sub_apps = [name for name in os.listdir(app_path) if
                        os.path.isdir(os.path.join(app_path, name))]

            for sub_app in sub_apps:
                sub_app_path = os.path.join(app_path, sub_app)
                tests_file = os.path.join(sub_app_path, "tests.py")

                if os.path.exists(tests_file):
                    app_and_sub_app = f"{app_name}.{sub_app}"
                    self.stdout.write(self.style.SUCCESS(f"Running tests for sub-app: {app_and_sub_app}"))
                    command = f"python manage.py test {app_and_sub_app}"
                    subprocess.call(command, shell=True)
                else:
                    self.stdout.write(
                        self.style.WARNING(f"No tests.py file found for app: {app_name}.{sub_app}. Skipping..."))
=======
import os
import subprocess

from django.apps import apps
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Run all tests in all sub-apps of all apps.'

    def handle(self, *args, **options):
        app_configs = apps.get_app_configs()
        for app_config in app_configs:
            app_name = app_config.name
            if app_name == 'simple_history':
                continue

            app_path = app_config.path
            sub_apps = [name for name in os.listdir(app_path) if
                        os.path.isdir(os.path.join(app_path, name))]

            for sub_app in sub_apps:
                sub_app_path = os.path.join(app_path, sub_app)
                tests_file = os.path.join(sub_app_path, "tests.py")

                if os.path.exists(tests_file):
                    app_and_sub_app = f"{app_name}.{sub_app}"
                    self.stdout.write(self.style.SUCCESS(f"Running tests for sub-app: {app_and_sub_app}"))
                    command = f"python manage.py test {app_and_sub_app}"
                    subprocess.call(command, shell=True)
                else:
                    self.stdout.write(
                        self.style.WARNING(f"No tests.py file found for app: {app_name}.{sub_app}. Skipping..."))
>>>>>>> origin/ma-branch
