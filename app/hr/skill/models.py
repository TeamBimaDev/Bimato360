from core.abstract.models import AbstractModel
from django.db import models
from hr.skill_category.models import SkillCategory
from hr.applicant.models import BimaHrApplicant


class BimaHrSkill(AbstractModel):
    name = models.CharField(max_length=255, unique=True)
    skill_categories = models.ForeignKey(SkillCategory, on_delete=models.CASCADE, default=1)
    applicant = models.ManyToManyField(BimaHrApplicant, related_name='BimaHrApplicantSkill', null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.name, self.public_id}"


    class Meta:
        permissions = []
