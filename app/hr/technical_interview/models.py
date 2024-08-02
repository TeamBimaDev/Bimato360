from common.enums.interview import get_interview_status_choices, get_interview_mode_choices
from core.abstract.models import AbstractModel
from django.db import models
from hr.candidat.models import BimaHrCandidat
from hr.vacancie.models import BimaHrVacancie
from hr.interview_step.models import BimaHrInterviewStep
from django.core.exceptions import ValidationError



class BimaHrTechnicalInterview(AbstractModel):
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, null=True)
    start_datetime = models.DateTimeField(null=True, blank=True)
    end_datetime = models.DateTimeField(null=True, blank=True)
    interview_mode = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_mode_choices())
    location = models.CharField(max_length=256, blank=True, null=True)
    status = models.CharField(max_length=64, blank=True, null=True, choices=get_interview_status_choices())
    candidat = models.ForeignKey(BimaHrCandidat, on_delete=models.CASCADE, default=1)
    vacancie = models.ForeignKey(BimaHrVacancie, on_delete=models.CASCADE, default=1)
    link_interview = models.URLField(max_length=200, blank=True, null=True)
    interview_step = models.ForeignKey(BimaHrInterviewStep, null=True, blank=True, on_delete=models.PROTECT)
    interviewers = models.ManyToManyField('BimaHrEmployee', through='BimaHrEmployeeinterviewer')
    record_path =  models.URLField(max_length=256, blank=True, null=True)
    id_event = models.CharField(max_length=256, blank=True, null=True)
 
    def __str__(self):
        return f"{self.title, self.vacancie.title, self.candidat.first_name}"
    
    def clean(self):
        super().clean()
        if self.start_datetime and self.end_datetime and self.start_datetime > self.end_datetime:
            raise ValidationError({
                'start_datetime': 'Start date and time must be before end date and time.',
                'end_datetime': 'End date and time must be after start date and time.'
            })


    class Meta:
        permissions = []

class BimaHrEmployeeinterviewer(AbstractModel):
    employee = models.ForeignKey('BimaHrEmployee', on_delete=models.CASCADE)
    technical_interview = models.ForeignKey('BimaHrTechnicalInterview', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.employee.first_name, self.employee.last_name, self.technical_interview.title}"

