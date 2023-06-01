from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from core.abstract.models import AbstractModel

from common.enums.company_type import get_company_type_choices
from common.enums.entity_status import get_entity_status_choices
from common.enums.gender import get_gender_choices
from common.enums.partner_type import get_partner_type_choices


class BimaErpPartner(AbstractModel):

    is_supplier = models.BooleanField(blank=True, null=True)
    is_customer = models.BooleanField(blank=True, null=True)
    partner_type = models.CharField(max_length=128, blank=False, null=False, choices=get_partner_type_choices())
    company_type = models.CharField(max_length=256, blank=True, null=True, choices=get_company_type_choices())
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    gender = models.CharField(max_length=32, blank=True, choices=get_gender_choices())
    social_security_number = models.CharField(max_length=64, blank=False, null=False)
    id_number = models.CharField(max_length=64, blank=False, null=False)
    Email = models.EmailField(blank=True, null=True)
    Phone = models.CharField(blank=True, null=True)
    Fax = models.CharField(blank=True, null=True)
    company_name = models.CharField(blank=True, null=True)
    company_activity = models.CharField(blank=True, null=True)
    vat_id_number = models.CharField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True, choices=get_entity_status_choices())
    note = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.public_id}"

from .signals import create_partner_related_entities