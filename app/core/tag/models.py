
from django.db import models
from core.abstract.models import AbstractModel


class BimaCoreTag(AbstractModel):
    name = models.CharField(max_length=128, blank=False, null=False)
    color = models.CharField(max_length=6, blank=True, null=True)
    parent = models.ForeignKey('self', null=True, blank=True,
                               on_delete=models.SET_NULL,
                               related_name='children')

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
