<<<<<<< HEAD
from common.enums.interview import get_interview_type_choices
from core.abstract.models import AbstractModel
from django.db import models


class BimaHrInterviewStep(AbstractModel):
    name = models.CharField(max_length=255)
    interview_type = models.CharField(max_length=100, blank=True, null=True, choices=get_interview_type_choices())
    description = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
=======
from common.enums.interview import get_interview_type_choices
from core.abstract.models import AbstractModel
from django.db import models


class BimaHrInterviewStep(AbstractModel):
    name = models.CharField(max_length=255)
    interview_type = models.CharField(max_length=100, blank=True, null=True, choices=get_interview_type_choices())
    description = models.CharField(max_length=256, blank=True, null=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        permissions = []
>>>>>>> origin/ma-branch
