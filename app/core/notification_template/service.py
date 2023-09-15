from .models import BimaCoreNotificationTemplate


class BimaCoreNotificationTemplateService:
    @staticmethod
    def get_notification_template_by_code(code):
        return BimaCoreNotificationTemplate.objects.filter(notification_type__code=code).first()

    @staticmethod
    def get_notification_template_by_public_id(type_public_id):
        return BimaCoreNotificationTemplate.objects.filter(notification_type__public_id=type_public_id).first()
