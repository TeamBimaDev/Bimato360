
from django.db import models
import uuid
from core.abstract.models import AbstractModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class BimaCoreAddress(AbstractModel):
    number = models.CharField(max_length=28, blank=False)
    street = models.CharField(max_length=256, blank=False)
    postal_code = models.CharField(max_length=28, blank=False)
    city = models.CharField(max_length=128, blank=False)
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


    def __str__(self) -> str:
        return f"{self.number ,self.city,self.street,self.postal_code}"

    class Meta:
        ordering = ['number']
        permissions = []
