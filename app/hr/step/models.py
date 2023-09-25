from core.abstract.models import AbstractModel
from django.db import models


class BimaHrInterviewStep(AbstractModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
