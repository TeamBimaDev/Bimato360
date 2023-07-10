from celery import shared_task
from .utils import generate_recurring_sale_documents


@shared_task
def generate_recurring_sale_documents_task():
    generate_recurring_sale_documents()