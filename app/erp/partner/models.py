from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from core.abstract.models import AbstractModel

from common.enums.partner_type import PartnerType
from common.enums.company_type import CompanyType
from common.enums.entity_status import EntityStatus
from common.enums.gender import Gender
from core.address.models import BimaCoreAddress
from core.contact.models import BimaCoreContact
from core.document.models import BimaCoreDocument


class BimaErpPartner(AbstractModel):
    GENDER_CHOICES = [(gender.value, gender.name) for gender in Gender]
    STATUS_CHOICES = [(status.value, status.name) for status in EntityStatus]
    PARTNER_TYPE_CHOICES = [(partner_type.value, partner_type.name) for partner_type in PartnerType]
    COMPANY_TYPE_CHOICES = [(company_type.value, company_type.name) for company_type in CompanyType]

    is_supplier = models.BooleanField(blank=True, null=True)
    is_customer = models.BooleanField(blank=True, null=True)
    partner_type = models.CharField(max_length=128, blank=False, null=False)
    company_type = models.CharField(max_length=256, blank=False, null=False)
    first_name = models.CharField(max_length=128, blank=False)
    last_name = models.CharField(max_length=128, blank=False)
    gender = models.CharField(max_length=32, blank=True, choices=GENDER_CHOICES)
    social_security_number = models.CharField(max_length=64, blank=False, null=False)
    id_number = models.CharField(max_length=64, blank=False, null=False)
    Email = models.EmailField(blank=True, null=True)
    Phone = models.CharField(blank=True, null=True)
    Fax = models.CharField(blank=True, null=True)
    company_name = models.CharField(blank=True, null=True)
    company_activity = models.CharField(blank=True, null=True)
    vat_id_number = models.CharField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True, choices=STATUS_CHOICES)
    note = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.public_id}"

from .signals import create_partner_related_entities