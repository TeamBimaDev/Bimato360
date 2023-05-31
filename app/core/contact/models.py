from django.db import models
from django.apps import apps
from core.abstract.models import AbstractModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from common.enums.gender import get_gender_choices


class BimaCoreContact(AbstractModel):
    name = models.CharField(max_length=256, blank=False, null=False,default="Si Ala")
    position = models.CharField(max_length=256, blank=True, null=True)
    department = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(max_length=128, blank=True, unique=False)
    mobile = models.CharField(max_length=128, blank=True, unique=False)
    phone = models.CharField(max_length=128, blank=True, unique=False)
    gender = models.CharField(max_length=32, blank=True, choices=get_gender_choices())
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

    def __str__(self):
        return self.mobile

    class Meta:
        ordering = ['mobile']
        permissions = []


def create_contact_from_parent_entity(data_contact_to_save, parent):
    for contact_data in data_contact_to_save:
        BimaCoreContact.objects.create(
            name=contact_data.get('name', ''),
            position=contact_data.get('position', ''),
            department=contact_data.get('department', ''),
            email=contact_data.get('email', ''),
            fax=contact_data.get('fax', ''),
            mobile=contact_data.get('mobile', ''),
            phone=contact_data.get('phone', ''),
            gender=contact_data.get('gender', ''),
            parent_type=ContentType.objects.get_for_model(parent),
            parent_id=parent.id
        )
