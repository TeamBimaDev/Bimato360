from django.db import models

# Create your models here.
from core.abstract.models import AbstractModel


class BimaPartners(AbstractModel):
    supplier = models.BooleanField(blank=True, null=True)
    customer = models.BooleanField(blank=True, null=True)
    name_supplier = models.BooleanField(blank=True, null=True)
    name_customer = models.BooleanField(blank=True, null=True)
    Email = models.EmailField(blank=True, null=True)
    Phone = models.CharField(blank=True, null=True)
    Fax = models.CharField(blank=True, null=True)

    def __str__(self):
        return f"{self.public_id}"