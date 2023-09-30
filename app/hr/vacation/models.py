from common.enums.vacation import get_vacation_type_list, get_vacation_status_list, VacationStatus
from core.abstract.models import AbstractModel
from django.db import models


class BimaHrVacation(AbstractModel):
    employee = models.ForeignKey('BimaHrEmployee', on_delete=models.CASCADE)
    manager = models.ForeignKey('BimaHrEmployee', related_name='managed_vacations', on_delete=models.SET_NULL,
                                null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    reason = models.TextField(null=True, blank=True)
    vacation_type = models.CharField(max_length=20, choices=get_vacation_type_list())
    status = models.CharField(max_length=20, choices=get_vacation_status_list(),
                              default=VacationStatus.PENDING.value)
    reason_refused = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.employee} from {self.date_start} to {self.date_end}"

    class Meta:
        permissions = []