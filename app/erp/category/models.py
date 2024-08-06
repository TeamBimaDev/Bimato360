from django.db import models

from core.abstract.models import AbstractModel


class BimaErpCategory(AbstractModel):
    name = models.CharField(max_length=255, blank=False, null=False, unique=True)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                 blank=True, related_name='children')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
