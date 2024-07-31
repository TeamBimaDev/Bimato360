from core.abstract.models import AbstractModel
from django.db import models
from hr.interview.models import BimaHrInterview

class BimaHrInterviewQuestion(AbstractModel):

    question = models.TextField(null=False)
    response = models.TextField(blank=True)
    video_path = models.FileField(upload_to="uploads/videos/", blank=True, null=True)
    interview = models.ForeignKey(BimaHrInterview, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.question}"

    class Meta:
        permissions = []
