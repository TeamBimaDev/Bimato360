from core.abstract.models import AbstractModel
from core.notification_type.models import BimaCoreNotificationType
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.utils.html import strip_tags


class BimaCoreNotification(AbstractModel):
    sender = models.ForeignKey(get_user_model(), related_name='sent_notifications', on_delete=models.PROTECT, null=True)
    receivers_email = models.JSONField(blank=True, null=True)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    attachments = models.JSONField(blank=True, null=True)
    date_sent = models.DateTimeField(auto_now_add=True)
    notification_type = models.ForeignKey(BimaCoreNotificationType, on_delete=models.CASCADE)

    parent_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    parent_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent_type', 'parent_id')

    class Meta:
        ordering = ['-date_sent']
        permissions = []
        default_permissions = ()

    def save(self, *args, **kwargs):
        if self.message:
            self.message = strip_tags(self.message)
        super().save(*args, **kwargs)
