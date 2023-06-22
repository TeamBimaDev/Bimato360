from django.db import models
from core.abstract.models import AbstractModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from common.enums.gender import get_gender_choices
from django.forms import model_to_dict
from rest_framework import status
from rest_framework.exceptions import ValidationError


class BimaCoreContact(AbstractModel):
    name = models.CharField(max_length=256, blank=False,
                            null=False, default="Si Ala")
    position = models.CharField(max_length=256, blank=True, null=True)
    department = models.CharField(max_length=256, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    fax = models.CharField(max_length=128, blank=True, unique=False)
    mobile = models.CharField(max_length=128, blank=True, unique=False)
    phone = models.CharField(max_length=128, blank=True, unique=False)
    gender = models.CharField(max_length=32, blank=True, null=True, choices=get_gender_choices())
    parent_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    parent_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self):
        return self.mobile

    class Meta:
        ordering = ['name']
        permissions = []


def create_contact_from_parent_entity(data_contact_to_save, parent):
    for contact_data in data_contact_to_save:
        create_single_contact(contact_data, parent)


def create_single_contact(contact_data, parent):
    try:
        contact = BimaCoreContact.objects.create(
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
        contact.refresh_from_db()
        contact_dict = model_to_dict(contact, exclude=["id", "parent_type", "parent_id"])
        return {"status": status.HTTP_201_CREATED, "data": contact_dict}
    except ValidationError as e:
        return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
    except Exception as e:
        return {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}


def get_contacts_for_parent_entity(parent):
    return BimaCoreContact.objects.filter(
        parent_type=ContentType.objects.get_for_model(parent),
        parent_id=parent.id
    )
