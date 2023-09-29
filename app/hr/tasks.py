import logging

from celery import shared_task
from django.db import transaction
from hr.employee.models import BimaHrEmployee
from hr.vacation.service import calculate_vacation_balances

logger = logging.getLogger(__name__)


@shared_task()
def update_all_employee_vacation_balances(secret_key=None):
    if secret_key != 'celer_beat_security_key_to_access_to_update_employee_vacation_balance':
        logger.error("Unauthorized access attempt to generate_recurring_sale_documents_task")
        return
    with transaction.atomic():
        for employee in BimaHrEmployee.objects.all():
            calculate_vacation_balances(employee)
