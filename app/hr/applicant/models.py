from core.abstract.models import AbstractModel
from core.source.models import BimaCoreSource
from django.db import models
from hr.step.models import BimaHrInterviewStep


class BimaHrApplicant(AbstractModel):
    priority = models.SmallIntegerField()
    availability_days = models.IntegerField()
    description = models.TextField(max_length=256)
    refuse = models.CharField(max_length=28, blank=False)
    comments = models.TextField(max_length=256)
    applicant_posts = models.ManyToManyField('hr.BimaHrPosition', through='hr.BimaHrApplicantPost')

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
    refuse = models.CharField(max_length=28, blank=False)
    comments = models.TextField(max_length=256)
    id_source_type = models.ForeignKey(BimaCoreSource, on_delete=models.CASCADE)
    source_name = models.TextField(max_length=256)
    score = models.FloatField()
    steps = models.ForeignKey(BimaHrInterviewStep, on_delete=models.CASCADE)
