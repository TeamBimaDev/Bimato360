<<<<<<< HEAD
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


class BimaHrPersonSkill(AbstractModel):
    person = models.ForeignKey(BimaHrPerson, on_delete=models.CASCADE)
    skill = models.ForeignKey(BimaHrSkill, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self) -> str:
        return f"{self.person} {self.skill} {self.level}"
=======
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


class BimaHrPersonSkill(AbstractModel):
    person = models.ForeignKey(BimaHrPerson, on_delete=models.CASCADE)
    skill = models.ForeignKey(BimaHrSkill, on_delete=models.CASCADE)
    level = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)])

    def __str__(self) -> str:
        return f"{self.person} {self.skill} {self.level}"
>>>>>>> origin/ma-branch
