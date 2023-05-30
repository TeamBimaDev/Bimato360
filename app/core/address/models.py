from django.db import models
from core.abstract.models import AbstractModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps
from core.country.models import BimaCoreCountry
from core.state.models import BimaCoreState


class BimaCoreAddress(AbstractModel):
    number = models.CharField(max_length=28, blank=False)
    street = models.CharField(max_length=256, blank=False)
    street2 = models.CharField(max_length=256, blank=True, null=True)
    zip = models.CharField(max_length=28, blank=False)
    city = models.CharField(max_length=128, blank=False)
    contact_name = models.CharField(max_length=256, blank=True, null=True)
    contact_phone = models.CharField(max_length=256, blank=True, null=True)
    contact_email = models.CharField(max_length=256, blank=True, null=True)
    can_send_bill = models.BooleanField(blank=True, null=True)
    can_deliver = models.BooleanField(blank=True, null=True)
    latitude = models.CharField(max_length=256, blank=True, null=True)
    longitude = models.CharField(max_length=256, blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    state = models.ForeignKey(BimaCoreState, on_delete=models.PROTECT)
    country = models.ForeignKey(BimaCoreCountry, on_delete=models.PROTECT)
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
        return f"{self.number, self.city, self.street, self.zip, self.country, self.state}"

    class Meta:
        ordering = ['number']
        permissions = []
