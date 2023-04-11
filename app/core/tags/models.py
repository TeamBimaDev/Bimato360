
from django.db import models
import uuid
from core.abstract.models import AbstractModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps

class BimaCoreTags(AbstractModel):
    name = models.CharField(max_length=256, blank=False)
    id_manager = models.IntegerField()
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
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
