import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "app.settings")
app = Celery("app")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'generate_recurring_sale_documents_task': {
        'task': 'erp.tasks.generate_recurring_sale_documents_task',
        'schedule': crontab(hour='11', minute='00'),
        'args': ('celer_beat_security_key_to_access_to_tasks',)
    },
    'verify_sale_document_payment_status_task': {
        'task': 'erp.tasks.verify_sale_document_payment_status_task',
        'schedule': crontab(hour='08', minute='00'),
        'args': ('celer_beat_security_key_to_access_to_payment_status_tasks',)
    },

}
