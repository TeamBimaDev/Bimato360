from core.abstract.models import AbstractModel
from django.db import models


class BimaHrJobCategory(AbstractModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='children')

    def __str__(self) -> str:
        return f"{self.name, self.id}"

    class Meta:
        ordering = ['name']
        permissions = []
