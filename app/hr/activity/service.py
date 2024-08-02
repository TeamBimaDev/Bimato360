from common.service.template_notification_service import BimaTemplateNotificationService
from core.notification_template.models import BimaCoreNotificationTemplate

from hr.activity.models import BimaHrActivityParticipant


class BimaHrActivityService:
    @staticmethod
    def group_by_date(history_data):
        grouped = defaultdict(list)

        for record in history_data:
            date_without_time = datetime.fromisoformat(record["history_date"]).date()
            grouped[date_without_time].append(record)

        return grouped


class BimaHrActivityNotificationService:

    @staticmethod
    def send_bulk_invitation_notifications(activity):
        participants = BimaHrActivityParticipant.objects.filter(activity=activity)
        for participant in participants:
            BimaHrActivityNotificationService.send_activity_invitation_notification(activity, participant)

    @staticmethod
    def send_activity_invitation_notification(activity, participant):
        notification_code = 'NOTIFICATION_ACTIVITY_INVITATION'
        notification_template, data_to_send = BimaHrActivityNotificationService.get_and_format_template(
            notification_code, activity, participant
        )
        data = BimaHrActivityNotificationService.prepare_data(notification_template, activity, data_to_send,
                                                              participant)
        BimaTemplateNotificationService.send_email_and_save_notification.delay(data)

    @staticmethod
    def prepare_data(notification_template, activity, data_to_send, participant):
        return {
            'subject': data_to_send['subject'],
            'message': data_to_send['message'],
            'receivers': [participant.person.email],
            'attachments': [],
            'notification_type_id': notification_template.notification_type.id,
            'sender': None,
            'app_name': 'hr',
            'model_name': 'bimahractivityparticipant',
            'parent_id': participant.id
        }

    @staticmethod
    def get_and_format_template(notification_code, activity, participant):
        template = BimaCoreNotificationTemplate.objects.filter(
            notification_type__code=notification_code
        ).first()
        if not template:
            raise ValueError("Notification template not found")

        data = {
            'person_full_name': participant.person.full_name,
            'activity_name': activity.name,
            'activity_start_date': activity.start_date,
            'activity_end_date': activity.end_date,
            'activity_description': activity.description,
        }

        formatted_message = BimaTemplateNotificationService.replace_variables_in_template(
            template.message, data
        )
        formatted_subject = BimaTemplateNotificationService.replace_variables_in_template(
            template.subject, data
        )
        return template, {'subject': formatted_subject, 'message': formatted_message, 'file_url': None}
