from core.abstract.models import AbstractModel
from django.db import models


class BimaHrActivityType(AbstractModel):
    name = models.CharField(max_length=28, blank=False)
    description = models.TextField()
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
