from company.models import BimaCompany
from core.abstract.models import AbstractModel
from core.notification_type.models import BimaCoreNotificationType
from django.db import models
from django.utils.html import strip_tags


class BimaCoreNotificationTemplate(AbstractModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    notification_type = models.ForeignKey(BimaCoreNotificationType, on_delete=models.CASCADE)
    company = models.ForeignKey(BimaCompany, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('notification_type',)
        ordering = ['name']
        permissions = []
        default_permissions = ()

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.message:
            self.message = strip_tags(self.message)
        super().save(*args, **kwargs)
