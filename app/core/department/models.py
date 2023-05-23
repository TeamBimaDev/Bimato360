from core.abstract.models import AbstractModel
from django.db import models
class BimaCoreDepartment(AbstractModel ):
    name = models.CharField(max_length=255)
    description = models.TextField()
    department = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    manager = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
