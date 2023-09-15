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
    'verify_purchase_document_payment_status_task': {
        'task': 'erp.tasks.verify_purchase_document_payment_status_task',
        'schedule': crontab(hour='08', minute='00'),
        'args': ('celer_beat_security_key_to_access_to_payment_status_tasks',)
    },
    'send_payment_late_sale_document_notification': {
        'task': 'core.tasks.send_notification_payment_late_sale_document',
        'schedule': crontab(hour='9', minute='50'),
        'args': ('celer_beat_security_key_to_access_to_payment_late_sale_document_notification_tasks',)
    },

}
