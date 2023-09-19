import logging

from celery import shared_task
from core.notification.service import BimaErpNotificationService

logger = logging.getLogger(__name__)


@shared_task()
def send_notification_for_payment_late_sale_documents(secret_key=None):
    if secret_key != 'celer_beat_security_key_to_access_to_payment_late_sale_document_notification_tasks':
        logger.error("Unauthorized access attempt to generate_recurring_sale_documents_task")
        return
    BimaErpNotificationService.send_notification_for_payment_late_sale_documents()


@shared_task()
def send_notification_for_payment_reminder_sale_documents(secret_key=None):
    if secret_key != 'celer_beat_security_key_to_access_to_payment_reminder_sale_document_notification_tasks':
        logger.error("Unauthorized access attempt to generate_recurring_sale_documents_task")
        return
    BimaErpNotificationService.send_notification_for_payment_reminder_sale_documents()
