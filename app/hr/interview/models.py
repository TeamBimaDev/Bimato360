from common.enums.interview import get_interview_status_choices
from core.abstract.models import AbstractModel
from django.db import models
from hr.applicant.models import BimaHrApplicantPost
from hr.interview_step.models import BimaHrInterviewStep


class BimaHrInterview(AbstractModel):
    date = models.DateField()
    note = models.TextField(max_length=255)
    score = models.FloatField(null=True, blank=True)
    comments = models.TextField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_status_choices())
    interview_step = models.ForeignKey(BimaHrInterviewStep, on_delete=models.PROTECT)
    applicant_post = models.ForeignKey(BimaHrApplicantPost, on_delete=models.CASCADE)
    refusal_reason = models.CharField(max_length=256, null=True, blank=True)
    refusal_date = models.DateField(null=True, blank=True)
    additional_comments = models.TextField(null=True, blank=True)
    interviewer = models.ForeignKey(
        'BimaHrEmployee',
        on_delete=models.SET_NULL,
        null=True,
        related_name='interviews_conducted'
    )
    refused_by = models.ForeignKey(
        'BimaHrEmployee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='interviews_refused'
    )

    def __str__(self):
        return self.date

    class Meta:
        ordering = ['-date']
        permissions = []
