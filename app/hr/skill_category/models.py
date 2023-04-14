from core.abstract.models import AbstractModel
from django.db import models

class SkillCategory(AbstractModel):
    name = models.CharField(max_length=100,unique=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    def __str__(self) -> str:
        return f"{self.name, self.id}"


    class Meta:
        ordering = ['name']
        verbose_name_plural = 'categories'
        permissions = []




