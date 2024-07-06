from core.abstract.models import AbstractModel
from django.db import models


class BimaCoreDepartment(AbstractModel):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    department = models.ForeignKey('self', on_delete=models.SET_NULL, null=True,
                                   blank=True, related_name='children')
    manager = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name} - {self.public_id}"

    class Meta:
        ordering = ['name']
        permissions = []
        default_permissions = ()
