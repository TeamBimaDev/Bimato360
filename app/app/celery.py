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
        'schedule': crontab(hour='08', minute='00'),
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
    'send_notification_for_payment_late_sale_documents': {
        'task': 'core.tasks.send_notification_for_payment_late_sale_documents',
        'schedule': crontab(hour='8', minute='00'),
        'args': ('celer_beat_security_key_to_access_to_payment_late_sale_document_notification_tasks',)
    },
    'send_notification_for_payment_reminder_sale_documents': {
        'task': 'core.tasks.send_notification_for_payment_reminder_sale_documents',
        'schedule': crontab(hour='8', minute='00'),
        'args': ('celer_beat_security_key_to_access_to_payment_reminder_sale_document_notification_tasks',)
    },

    'update_all_employee_vacation_balances': {
        'task': 'hr.tasks.update_all_employee_vacation_balances',
        'schedule': crontab(minute='0', hour='0', day_of_month='1'),
        'args': ('celer_beat_security_key_to_access_to_update_employee_vacation_balance',)
    },

}
