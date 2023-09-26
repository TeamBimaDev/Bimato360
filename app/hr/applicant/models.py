from common.enums.interview import get_interview_status_choices
from core.abstract.models import AbstractModel
from core.source.models import BimaCoreSource
from django.db import models
from hr.interview_step.models import BimaHrInterviewStep
from hr.models import BimaHrPerson


class BimaHrApplicant(BimaHrPerson):
    priority = models.SmallIntegerField()
    availability_days = models.IntegerField()
    description = models.TextField(max_length=256)
    comments = models.TextField(max_length=256)
    applicant_posts = models.ManyToManyField('BimaHrPosition', through='BimaHrApplicantPost')

    def __str__(self):
        return self.full_name

    class Meta:
        ordering = ['first_name']
        permissions = []


class BimaHrApplicantPost(AbstractModel):
    position = models.ForeignKey('BimaHrPosition', on_delete=models.CASCADE)
    applicant = models.ForeignKey('BimaHrApplicant', on_delete=models.CASCADE)
    expected_salary = models.FloatField(blank=True, null=True, default=None)
    proposed_salary = models.FloatField(blank=True, null=True, default=None)
    accepted_salary = models.FloatField(blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(max_length=256)
    source_type = models.ForeignKey(BimaCoreSource, on_delete=models.CASCADE, null=True, blank=True, default=None)
    source_name = models.TextField(max_length=256, null=True, blank=True, default=None)
    score = models.FloatField(null=True, blank=True, default=None)
    interview_step = models.ForeignKey(BimaHrInterviewStep, on_delete=models.CASCADE)
    status = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_status_choices())
