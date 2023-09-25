from core.abstract.models import AbstractModel
from django.db import models
from hr.models import BimaHrPerson
from hr.skill_category.models import BimaHrSkillCategory


class BimaHrSkill(AbstractModel):
    name = models.CharField(max_length=255, unique=True)
    skill_categories = models.ForeignKey(BimaHrSkillCategory, on_delete=models.CASCADE)
    persons = models.ManyToManyField(BimaHrPerson, through='BimaHrPersonSkill')

    def __str__(self) -> str:
        return f"{self.name, self.public_id}"

    class Meta:
        permissions = []
