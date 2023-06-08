from django.db import models

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.abstract.models import AbstractModel
from core.tag.models import BimaCoreTag
from rest_framework import status
from rest_framework.exceptions import ValidationError


class BimaCoreEntityTag(AbstractModel):
    tag = models.ForeignKey(BimaCoreTag, on_delete=models.PROTECT)
    id_manager = models.IntegerField(blank=True, null=True)
    parent_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    parent_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self) -> str:
        return f"{self.public_id} - {self.tag.name}"

    class Meta:
        ordering = ['-created']
        permissions = []


def create_entity_tag_from_parent_entity(data_entity_tag_to_save, parent):
    for tag_data in data_entity_tag_to_save:
        create_single_entity_tag(tag_data, parent)


def create_single_entity_tag(tag_data, parent):
    tag = BimaCoreTag.objects.get_object_by_public_id(tag_data['tag_public_id'])

    try:
        item = BimaCoreEntityTag.objects.create(
            id_manager=tag_data.get('id_manager', ''),
            tag=tag,
            parent_type=ContentType.objects.get_for_model(parent),
            parent_id=parent.id,
        )
        return item

    except ValidationError as e:
        return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
    except Exception as e:
        return {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}


def get_entity_tags_for_parent_entity(parent):
    return BimaCoreEntityTag.objects.select_related('tag').filter(
        parent_type=ContentType.objects.get_for_model(parent),
        parent_id=parent.id
    )
