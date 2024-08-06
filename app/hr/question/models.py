from core.abstract.models import AbstractModel
from django.db import models
from hr.question_category.models import BimaHrQuestionCategory


class BimaHrQuestion(AbstractModel):
    question = models.TextField(unique=True)
    question_category = models.ForeignKey(BimaHrQuestionCategory, on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
   
    def __str__(self) -> str:
        return f"{self.name}"

    class Meta:
        permissions = []


