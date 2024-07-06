from company.models import BimaCompany
from core.abstract.models import AbstractModel
from core.notification_type.models import BimaCoreNotificationType
from django.db import models
from django.utils.translation import gettext_lazy as _


class BimaCoreNotificationTemplate(AbstractModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    notification_type = models.OneToOneField(BimaCoreNotificationType, on_delete=models.CASCADE,
                                             error_messages={
                                                 'unique': _("A template with this notification type already exists.")
                                             })
    company = models.ForeignKey(BimaCompany, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()

    def __str__(self) -> str:
        return self.name
