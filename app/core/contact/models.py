
from django.db import models
from django.apps import apps
from core.abstract.models import AbstractModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

class BimaCoreContact(AbstractModel):
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(max_length=128, blank=False, unique=True)
    mobile = models.CharField(max_length=128, blank=False, unique=True)
    phone = models.CharField(max_length=128, blank=False, unique=True)
    parent_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE,
        limit_choices_to={
            'app_label__in': [
                app_config.label for app_config in apps.get_app_configs()
                if app_config.label not in ['admin', 'auth', 'contenttypes', 'sessions', 'auditlog']
            ]
        }
    )
    parent_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self) :
        return self.mobile

    class Meta:
        ordering = ['mobile']
        permissions = []
