
from django.db import models

from core.abstract.models import AbstractModel


class BimaCoreBank(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    email = models.EmailField(blank=True, null=True)
    active = models.BooleanField(default=True)
    bic = models.CharField(max_length=16, blank=False, null=False)

    def __str__(self):
        return f"{self.name ,self.public_id, self.id}"

    class Meta:
        ordering = ['name']
        permissions = []
