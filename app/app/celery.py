import os
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate_recurring_sale_documents': {
        'task': 'erp.sale_document.tasks.generate_recurring_sale_documents',
        'schedule': crontab(hour=8, minute=30),
    },
}
