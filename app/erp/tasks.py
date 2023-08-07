import logging

from celery import shared_task
from erp.sale_document.service import generate_recurring_sale_documents

logger = logging.getLogger(__name__)


@shared_task()
def generate_recurring_sale_documents_task(secret_key=None):
    if secret_key != 'celer_beat_security_key_to_access_to_tasks':
        logger.error("Unauthorized access attempt to generate_recurring_sale_documents_task")
        return
    generate_recurring_sale_documents()
