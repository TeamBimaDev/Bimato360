from django.db import models
from core.abstract.models import AbstractModel
class BimaHrActivityType(AbstractModel):
    name = models.CharField(max_length=28, blank=False)
    description = models.TextField()
