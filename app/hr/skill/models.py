from core.abstract.models import AbstractModel
from django.db import models
from hr.models import BimaHrPerson
from hr.skill_category.models import BimaHrSkillCategory


class BimaHrSkill(AbstractModel):
    name = models.CharField(max_length=255, unique=True)
    skill_category = models.ForeignKey(BimaHrSkillCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    persons = models.ManyToManyField(BimaHrPerson, through='BimaHrPersonSkill')

    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        permissions = []
