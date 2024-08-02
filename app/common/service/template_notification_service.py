

import re
from decimal import Decimal

from celery import shared_task
from common.email.email_service import EmailService
from core.notification.models import BimaCoreNotification
from core.notification_type.models import BimaCoreNotificationType
from django.contrib.contenttypes.models import ContentType


class BimaTemplateNotificationService:
    @staticmethod
    def replace_variables_in_template(template, data):
        pattern = r'\{\{(\w+)\}\}'

        def replace_variable(match):
            variable_name = match.group(1)
            if variable_name in data:
                value = data[variable_name]

                if variable_name == 'due_date':
                    formatted_due_date = ''
                    for due_date_entry in value:
                        due_date, percentage = list(due_date_entry.items())[0]
                        percentage_amount = (Decimal(percentage) / 100) * data.get('total_amount', 0)
                        formatted_due_date += f"Date d'échéance : {due_date.strftime('%Y/%m/%d')} : {percentage}% ({percentage_amount})" + "<br/>"

                    return formatted_due_date

                return str(value)

            return match.group(0)

        replaced_template = re.sub(pattern, replace_variable, template)

        return replaced_template

    @staticmethod
    @shared_task(bind=True, max_retries=3, soft_time_limit=500)
    def send_email_and_save_notification(task, data):
        subject = data['subject']
        message = data['message']
        receivers = data['receivers']
        attachments = data['attachments']
        notification_type_id = data.get('notification_type_id')
        sender = data['sender']
        app_name = data['app_name']
        model_name = data['model_name']
        parent_id = data['parent_id']

        if EmailService.send_email(subject, message, receivers, attachments=attachments, html_message=True):
            BimaTemplateNotificationService.save_notification(
                receivers=receivers,
                subject=subject,
                message=message,
                attachments=attachments,
                notification_type_id=notification_type_id,
                sender=sender,
                app_name=app_name,
                model_name=model_name,
                parent_id=parent_id
            )

    @staticmethod
    def save_notification(receivers, subject, message, attachments, notification_type_id, sender=None, app_name=None,
                          model_name=None, parent_id=None):

        try:
            parent_type = ContentType.objects.get(app_label=app_name, model=model_name)
        except ContentType.DoesNotExist:
            parent_type = None

        notification_type = BimaCoreNotificationType.objects.get(id=notification_type_id)

        notification = BimaCoreNotification.objects.create(
            sender=sender,
            receivers_email=receivers,
            subject=subject,
            message=message,
            attachments=attachments,
            notification_type=notification_type,
            parent_type=parent_type,
            parent_id=parent_id
        )

        return notification


