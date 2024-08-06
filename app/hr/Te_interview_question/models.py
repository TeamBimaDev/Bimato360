from core.abstract.models import AbstractModel
from django.db import models
from hr.technical_interview.models import BimaHrTechnicalInterview

class BimaHrTechnicalInterviewQuestion(AbstractModel):

    question_te = models.TextField(null=False)
    response_te = models.TextField(blank=True)
    interview_te = models.ForeignKey(BimaHrTechnicalInterview, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.question_te}"

    class Meta:
        permissions = []
