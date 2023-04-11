
from django.db import models
from core.abstract.models import AbstractModel

class BimaHrInterviewStep(AbstractModel):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=256, blank=True, null=True)


    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []





