from core.abstract.serializers import AbstractSerializer
from core.notification_type.models import BimaCoreNotificationType
from rest_framework import serializers

from .models import BimaCoreNotification


class BimaCoreNotificationSerializer(AbstractSerializer):
    notification_type = serializers.SerializerMethodField(read_only=True)
    notification_type_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreNotificationType.objects.all(),
        slug_field='public_id',
        source='notification_type',
        write_only=True
    )

    def get_notification_type(self, obj):
        return {
            'id': obj.notification_type.public_id.hex,
            'code': obj.notification_type.code,
            'name': obj.notification_type.name
        }

    class Meta:
        model = BimaCoreNotification
        fields = (
            'id', 'sender', 'receivers_email', 'subject', 'message', 'attachments', 'date_sent',
            'notification_type', 'notification_type_public_id', 'created', 'updated',
        )
