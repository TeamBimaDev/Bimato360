from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from django.shortcuts import get_object_or_404

from core.abstract.models import AbstractModel
from core.tag.models import BimaCoreTag


class BimaCoreEntityTag(AbstractModel):
    tag = models.ForeignKey(BimaCoreTag, on_delete=models.PROTECT)
    id_manager = models.IntegerField(blank=True, null=True)
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


def create_entity_tag_from_parent_entity(data_entity_tag_to_save, parent):
    for tag_data in data_entity_tag_to_save:
        tag = get_object_or_404(BimaCoreTag, public_id=tag_data['tag'])

        BimaCoreEntityTag.objects.create(
            id_manager=tag_data.get('id_manager', ''),
            tag_id=tag.id,
            parent_type=ContentType.objects.get_for_model(parent),
            parent_id=parent.id,
        )
