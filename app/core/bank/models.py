
from core.abstract.models import AbstractModel
from django.db import models


class BimaCoreBank(AbstractModel):
    name = models.CharField(max_length=128, blank=False, unique=True)
    email = models.EmailField(blank=True, null=True, unique=True)
    active = models.BooleanField(default=True)
    bic = models.CharField(max_length=16, blank=False, null=False, unique=True)

    def __str__(self):
        return f"{self.name, self.public_id}"

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
