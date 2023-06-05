from django.db import models
from core.abstract.models import AbstractModel


class BimaCoreTag(AbstractModel):
    name = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
