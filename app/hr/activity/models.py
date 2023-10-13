from common.enums.activity_status import get_activity_status_choices, get_presence_status_choices, ActivityStatus, \
    PresenceStatus
from core.abstract.models import AbstractModel
from django.db import models
from hr.activity_type.models import BimaHrActivityType
from hr.employee.models import BimaHrEmployee
from hr.models import BimaHrPerson
from rest_framework.exceptions import ValidationError
from simple_history.models import HistoricalRecords


class BimaHrActivity(AbstractModel):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=get_activity_status_choices(), null=False, blank=False,
                              default=ActivityStatus.IN_PROGRESS.name)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    activity_type = models.ForeignKey(BimaHrActivityType, on_delete=models.CASCADE)
    organizer = models.ForeignKey(BimaHrEmployee, on_delete=models.CASCADE)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name, self.activity_type.name}"

    def save(self, *args, **kwargs):
        if self.end_date <= self.start_date:
            raise ValidationError("End Date must be greater than Start Date")
        super().save(*args, **kwargs)


class BimaHrActivityParticipant(AbstractModel):
    activity = models.ForeignKey(BimaHrActivity, on_delete=models.CASCADE)
    person = models.ForeignKey(BimaHrPerson, on_delete=models.CASCADE)
    presence_status = models.CharField(max_length=20, choices=get_presence_status_choices(), null=True, blank=True,
                                       default=PresenceStatus.NOT_SPECIFIED.name)

    def __str__(self):
        return f"{self.activity.name, self.person.full_name, self.presence_status}"
