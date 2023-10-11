import logging

from celery import shared_task
from django.db import transaction
from hr.employee.models import BimaHrEmployee
from hr.vacation.service import calculate_vacation_balances
from hr.vacation.service import update_expired_vacations

logger = logging.getLogger(__name__)


@shared_task()
def update_all_employee_vacation_balances(secret_key=None):
    if secret_key != 'celer_beat_security_key_to_access_to_update_employee_vacation_balance':
        logger.error("Unauthorized access attempt to generate_recurring_sale_documents_task")
        return
    with transaction.atomic():
        for employee in BimaHrEmployee.objects.all():
            employee_old_vacation_balance = employee.balance_vacation
            employee_old_virtual_vacation_balance = employee.virtual_balance_vacation
            calculate_vacation_balances(employee)
            employee_new_vacation_balance = employee.balance_vacation
            employee_new_virtual_vacation_balance = employee.virtual_balance_vacation
            logger.info(
                {"employee_public_id": employee.public_id,
                 "employee_full_name": employee.full_name,
                 "old_vacation_balance": employee_old_vacation_balance,
                 "new_vacation_balance": employee_new_vacation_balance,
                 "old_virtual_vacation_balance": employee_old_virtual_vacation_balance,
                 "new_virtual_vacation_balance": employee_new_virtual_vacation_balance
                 })


@shared_task()
def update_expired_vacations_task(secret_key=None):
    if secret_key != 'celer_beat_security_key_to_access_to_update_expired_vacations_tasks':
        logger.error("Unauthorized access attempt to verify_purchase_document_payment_status_task")
        return
    update_expired_vacations()
