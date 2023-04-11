
from django.db import models

from core.abstract.models import AbstractModel
from core.country.models import BimaCoreCountry
from core.state.models import BimaCoreState


class BimaCoreBank(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    street = models.CharField(max_length=256, blank=True, null=True)
    street2 = models.CharField(max_length=256, blank=True, null=True)
    zip = models.CharField(max_length=16, blank=True, null=True)
    city = models.CharField(max_length=16, blank=True, null=True)
    state = models.ForeignKey(
        BimaCoreState, on_delete=models.PROTECT)
    country = models.ForeignKey(
        BimaCoreCountry, on_delete=models.PROTECT)
    email = models.EmailField(blank=True, null=True)
    active = models.BooleanField(default=True)
    bic = models.CharField(max_length=16, blank=True, null=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
