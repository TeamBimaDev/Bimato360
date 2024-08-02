

from core.abstract.serializers import AbstractSerializer

from .models import BimaCoreNotificationType


class BimaCoreNotificationTypeSerializer(AbstractSerializer):
    class Meta:
        model = BimaCoreNotificationType
        fields = [
            'id', 'name', 'active', 'code', 'is_system', 'created', 'updated'
        ]
        read_only_fields = ('code', 'is_system')


