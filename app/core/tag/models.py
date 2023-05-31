from django.db import models
import uuid
from core.abstract.models import AbstractModel
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.apps import apps


class BimaCoreTag(AbstractModel):
    name = models.CharField(max_length=128, blank=False, null=False)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
