
from django.db import models
from core.abstract.models import AbstractModel
from hr.step.models import BimaHrInterviewStep
from hr.applicant.models import BimaHrApplicant


class BimaHrInterview(AbstractModel):
    name = models.CharField(max_length=28, blank=False)
    date = models.DateTimeField()
    steps = models.ForeignKey(BimaHrInterviewStep, on_delete=models.PROTECT)
    id_interviewer = models.IntegerField()
    note = models.TextField(max_length=255)
    score = models.SmallIntegerField()
    result = models.SmallIntegerField()
    applicant = models.ForeignKey(BimaHrApplicant, on_delete=models.PROTECT)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []

