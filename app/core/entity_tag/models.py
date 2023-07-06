from django.db import models
from django.db import transaction
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from core.abstract.models import AbstractModel
from core.tag.models import BimaCoreTag
from rest_framework import status
from rest_framework.exceptions import ValidationError


class BimaCoreEntityTag(AbstractModel):
    tag = models.ForeignKey(BimaCoreTag, on_delete=models.PROTECT)
    id_manager = models.IntegerField(blank=True, null=True)
    order = models.PositiveIntegerField(blank=True, null=True, default=1)
    parent_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    parent_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self) -> str:
        return f"{self.public_id} - {self.tag.name} - {self.order} "

    class Meta:
        ordering = ['-created']
        permissions = []
        default_permissions = ()


def create_entity_tag_from_parent_entity(data_entity_tag_to_save, parent):
    for tag_data in data_entity_tag_to_save:
        create_single_entity_tag(tag_data, parent)


def create_single_entity_tag(tag_data, parent):
    try:
        with transaction.atomic():
            tag = get_tag(tag_data)
            parent_type = get_parent_type(parent)

            if entity_tag_exists(tag, parent_type, parent.id):
                return {"error": "Item already exists", "status": status.HTTP_400_BAD_REQUEST}

            order = get_order(tag_data, parent_type, parent.id)

            item = save_entity_tag(tag_data, tag, order, parent_type, parent.id)

            return item

    except ValidationError as e:
        return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
    except Exception as e:
        return {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}


def get_tag(tag_data):
    return BimaCoreTag.objects.get_object_by_public_id(tag_data['tag_public_id'])


def get_parent_type(parent):
    return ContentType.objects.get_for_model(parent)


def entity_tag_exists(tag, parent_type, parent_id):
    return BimaCoreEntityTag.objects.filter(tag=tag, parent_type=parent_type, parent_id=parent_id).exists()


def get_order(tag_data, parent_type, parent_id):
    total_tags = BimaCoreEntityTag.objects.filter(
        parent_type=parent_type,
        parent_id=parent_id
    ).count()

    try:
        order = int(tag_data.get("order"))

        if order <= 0 or order > total_tags:
            return total_tags + 1

        existing_orders = BimaCoreEntityTag.objects.filter(
            parent_type=parent_type,
            parent_id=parent_id
        ).values_list('order', flat=True)

        if order in existing_orders:
            BimaCoreEntityTag.objects.filter(
                parent_type=parent_type,
                parent_id=parent_id,
                order__gte=order
            ).update(order=models.F('order') + 1)

    except (ValueError, TypeError):
        # If the order is not a number, set it to the end of the list.
        return total_tags + 1

    return order


def save_entity_tag(tag_data, tag, order, parent_type, parent_id):
    return BimaCoreEntityTag.objects.create(
        id_manager=tag_data.get('id_manager', 0),
        tag=tag,
        order=order,
        parent_type=parent_type,
        parent_id=parent_id,
    )


def get_entity_tags_for_parent_entity(parent):
    return BimaCoreEntityTag.objects.select_related('tag').filter(
        parent_type=ContentType.objects.get_for_model(parent),
        parent_id=parent.id
    )
