from core.abstract.models import AbstractModel
from django.db import models
from hr.activity_type.models import BimaHrActivityType
from hr.applicant.models import BimaHrApplicant
from simple_history.models import HistoricalRecords
from common.enums.activity_status import get_activity_status_choices
from hr.employee.models import BimaHrEmployee


class BimaHrActivity(AbstractModel):
    name = models.CharField(max_length=28, blank=False)
    description = models.TextField()
    activity_status = models.CharField(max_length=20, choices=get_activity_status_choices(), null=False, blank=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    id_manager = models.IntegerField()
    activity_type = models.ForeignKey(BimaHrActivityType, on_delete=models.CASCADE)
    employee = models.ForeignKey(BimaHrEmployee, on_delete=models.CASCADE)
    history = HistoricalRecords()
    def __str__(self):
        return f"{self.name, self.activity_type.name}"
