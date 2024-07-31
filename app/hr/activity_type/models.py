<<<<<<< HEAD
from core.abstract.models import AbstractModel
from django.db import models


class BimaHrActivityType(AbstractModel):
    name = models.CharField(max_length=28, blank=False)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
=======
from core.abstract.models import AbstractModel
from django.db import models


class BimaHrActivityType(AbstractModel):
    name = models.CharField(max_length=28, blank=False)
    description = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
>>>>>>> origin/ma-branch
