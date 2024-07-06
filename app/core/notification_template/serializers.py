import bleach
from company.models import BimaCompany
from core.abstract.serializers import AbstractSerializer
from core.notification_type.models import BimaCoreNotificationType
from rest_framework import serializers

from app import settings
from .models import BimaCoreNotificationTemplate


class BimaCoreNotificationTemplateSerializer(AbstractSerializer):
    raw_html_message = serializers.CharField(source='message', required=False, allow_blank=True)
    notification_type = serializers.SerializerMethodField(read_only=True)
    notification_type_public_id = serializers.SlugRelatedField(
        queryset=BimaCoreNotificationType.objects.all(),
        slug_field='public_id',
        source='notification_type',
        write_only=True
    )

    company = serializers.SerializerMethodField(read_only=True)
    company_public_id = serializers.SlugRelatedField(
        queryset=BimaCompany.objects.all(),
        slug_field='public_id',
        source='company',
        write_only=True
    )

    def get_notification_type(self, obj):
        return {
            'id': obj.notification_type.public_id.hex,
            'code': obj.notification_type.code,
            'name': obj.notification_type.name
        }

    def validate_raw_html_message(self, value):
        allowed_tags = settings.html_allowed_tags
        return bleach.clean(value, strip=True, tags=list(bleach.sanitizer.ALLOWED_TAGS) + allowed_tags)

    def get_company(self, obj):
        return {
            'id': obj.company.public_id.hex,
            'name': obj.company.name
        }

    class Meta:
        model = BimaCoreNotificationTemplate
        fields = (
            'id', 'name', 'subject', 'raw_html_message', 'notification_type', 'notification_type_public_id', 'company',
            'company_public_id', 'created', 'updated',
        )
