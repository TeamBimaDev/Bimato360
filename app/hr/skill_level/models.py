from core.abstract.models import AbstractModel
from django.db import models


class SkillLevel(AbstractModel):
    name = models.CharField(max_length=255 ,unique=True)


    def __str__(self) -> str:
        return self.name






