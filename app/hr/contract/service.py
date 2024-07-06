import logging
from collections import defaultdict
from datetime import datetime

from common.enums.position import ContractStatus
from common.service.template_notification_service import BimaTemplateNotificationService
from core.notification_template.models import BimaCoreNotificationTemplate
from django.contrib.auth import get_user_model
from django.db import transaction, IntegrityError
from django.utils import timezone
from hr.contract.models import BimaHrContract

logger = logging.getLogger(__name__)


class BimaHrContractService:
    @staticmethod
    def group_by_date(history_data):
        grouped = defaultdict(list)

        for record in history_data:
            date_without_time = datetime.fromisoformat(record["history_date"]).date()
            grouped[date_without_time].append(record)

        return grouped


class BimaContractNotificationService:

    @staticmethod
    def send_contract_expiry_notifications():
        today = timezone.localdate()

        active_contracts = BimaHrContract.objects.filter(
            status=ContractStatus.ACTIVE.name,
            end_date__isnull=False
        )

        for contract in active_contracts:
            remaining_days = (contract.end_date - today).days
            if remaining_days in [30, 15]:
                BimaContractNotificationService.send_notification(contract, remaining_days)

    @staticmethod
    def send_notification(contract, remaining_days):
        notification_template, data_to_send = BimaContractNotificationService.get_and_format_template(
            'NOTIFICATION_CONTRACT_EXPIRY_SOON', contract, remaining_days
        )
        data = BimaContractNotificationService.prepare_data(notification_template, contract, data_to_send)
        BimaTemplateNotificationService.send_email_and_save_notification.delay(data)

    @staticmethod
    def prepare_data(notification_template, contract, data_to_send):
        all_users = get_user_model().objects.all()
        users_with_permission = [user for user in all_users if user.has_perm('hr.contract.can_manage_others_contract')]

        return {
            'subject': data_to_send['subject'],
            'message': data_to_send['message'],
            'receivers': [user.email for user in users_with_permission],
            'attachments': [],
            'notification_type_id': notification_template.notification_type.id,
            'sender': None,
            'app_name': 'hr',
            'model_name': 'bimahrcontract',
            'parent_id': contract.id
        }

    @staticmethod
    def get_and_format_template(notification_code, contract, remaining_days):
        template = BimaCoreNotificationTemplate.objects.filter(
            notification_type__code=notification_code
        ).first()
        if not template:
            raise ValueError("Notification template not found")

        data = {
            'employee_full_name': contract.employee.full_name,
            'department_name': contract.department.name if contract.department else '',
            'remaining_days': remaining_days,
            'contract_end_date': contract.end_date
        }

        formatted_message = BimaTemplateNotificationService.replace_variables_in_template(
            template.message, data
        )
        formatted_subject = BimaTemplateNotificationService.replace_variables_in_template(
            template.subject, data
        )
        return template, {'subject': formatted_subject, 'message': formatted_message}

    @staticmethod
    def update_expired_vacations():
        try:
            with transaction.atomic():
                today = timezone.localdate()
                active_contracts = BimaHrContract.objects.filter(status=ContractStatus.ACTIVE.name)
                updated_count = 0
                for contract in active_contracts:
                    if contract.end_date < today:
                        contract.status = ContractStatus.EXPIRED.name
                        contract.save()
                        updated_count += 1

                logger.info(f'Successfully updated {updated_count} vacation(s) to expired status.')

        except IntegrityError as e:
            logger.error(f'Database error while updating expired vacations: {e}')

        except Exception as e:
            logger.error(f'Unexpected error while updating expired vacations: {e}')
