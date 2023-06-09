from django.db import models

from core.abstract.models import AbstractModel


class BimaErpCategory(AbstractModel):
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(null=True, default=True)
    category = models.ForeignKey('self', on_delete=models.CASCADE, null=True,
                                 blank=True, related_name='category_children')

    def __str__(self) -> str:
        return self.name
    class Meta:
        ordering = ['name']
        permissions = []