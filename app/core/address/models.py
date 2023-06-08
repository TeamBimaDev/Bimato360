from django.db import models
from core.abstract.models import AbstractModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from core.country.models import BimaCoreCountry
from core.state.models import BimaCoreState
from rest_framework import status
from rest_framework.exceptions import ValidationError


class BimaCoreAddress(AbstractModel):
    number = models.CharField(max_length=28, blank=False)
    street = models.CharField(max_length=256, blank=False)
    street2 = models.CharField(max_length=256, blank=True, null=True)
    zip = models.CharField(max_length=28, blank=False)
    city = models.CharField(max_length=128, blank=False)
    contact_name = models.CharField(max_length=256, blank=True, null=True)
    contact_phone = models.CharField(max_length=256, blank=True, null=True)
    contact_email = models.EmailField(max_length=256, blank=True, null=True)
    can_send_bill = models.BooleanField(blank=True, null=True)
    can_deliver = models.BooleanField(blank=True, null=True)
    latitude = models.CharField(max_length=256, blank=True, null=True)
    longitude = models.CharField(max_length=256, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    state = models.ForeignKey(BimaCoreState, on_delete=models.PROTECT)
    country = models.ForeignKey(BimaCoreCountry, on_delete=models.PROTECT)
    parent_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    parent_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('parent_type', 'parent_id')

    def __str__(self):
        return f"{self.number, self.city, self.street, self.zip, self.country, self.state}"

    class Meta:
        ordering = ['number']
        permissions = []


def create_address_from_parent_entity(data_address_to_save, parent):
    for address_data in data_address_to_save:
        create_single_address(address_data, parent)


def create_single_address(address_data, parent):
    try:
        state = BimaCoreState.objects.get_object_by_public_id(address_data.get('state_public_id'))
        country = BimaCoreCountry.objects.get_object_by_public_id(address_data.get('country_public_id'))
        BimaCoreAddress.objects.create(
            number=address_data.get('number', ''),
            street=address_data.get('street', ''),
            street2=address_data.get('street2', ''),
            zip=address_data.get('zip', ''),
            city=address_data.get('city', ''),
            contact_name=address_data.get('contact_name', ''),
            contact_phone=address_data.get('contact_phone', ''),
            contact_email=address_data.get('contact_email', ''),
            can_send_bill=address_data.get('can_send_bill', ''),
            can_deliver=address_data.get('can_deliver', ''),
            latitude=address_data.get('latitude', ''),
            longitude=address_data.get('longitude', ''),
            note=address_data.get('note', ''),
            state=state,
            country=country,
            parent_type=ContentType.objects.get_for_model(parent),
            parent_id=parent.id
        )
        return True

    except ValidationError as e:
        return {"error": str(e), "status": status.HTTP_400_BAD_REQUEST}
    except Exception as e:
        return {"error": str(e), "status": status.HTTP_500_INTERNAL_SERVER_ERROR}


def get_addresses_for_parent(parent):
    return BimaCoreAddress.objects.filter(
        parent_type=ContentType.objects.get_for_model(parent),
        parent_id=parent.id
    )
