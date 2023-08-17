from company.models import BimaCompany
from core.abstract.models import AbstractModel
from django.db import models


class BimaTreasuryCash(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    active = models.BooleanField(default=True)
    company = models.ForeignKey(BimaCompany, on_delete=models.PROTECT)
    note = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['id']
        permissions = []
        default_permissions = ()
