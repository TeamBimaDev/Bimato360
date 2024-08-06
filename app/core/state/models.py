from django.db import models

from core.abstract.models import AbstractModel
from core.country.models import BimaCoreCountry


class BimaCoreState(AbstractModel):
    name = models.CharField(max_length=128, blank=False)
    code = models.CharField(max_length=256, blank=True, null=True)
    country = models.ForeignKey(
        BimaCoreCountry, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.name ,self.id}"

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
