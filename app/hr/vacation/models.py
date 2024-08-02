from common.enums.vacation import get_vacation_type_list, get_vacation_status_list, VacationStatus
from common.service.bima_service import BimaService
from core.abstract.models import AbstractModel
from django.db import models
from django.utils import timezone


class BimaHrVacation(AbstractModel):
    employee = models.ForeignKey('BimaHrEmployee', on_delete=models.CASCADE)
    manager = models.ForeignKey('BimaHrEmployee', related_name='managed_vacations', on_delete=models.SET_NULL,
                                null=True)
    date_start = models.DateField()
    date_end = models.DateField()
    reason = models.TextField(null=True, blank=True)
    vacation_type = models.CharField(max_length=20, choices=get_vacation_type_list())
    status = models.CharField(max_length=20, choices=get_vacation_status_list(),
                              default=VacationStatus.PENDING.name)
    reason_refused = models.TextField(null=True, blank=True)
    request_date = models.DateTimeField(auto_now_add=True)
    status_change_date = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.employee} from {self.date_start} to {self.date_end}"

    def save(self, *args, **kwargs):
        # self._verify_if_date_expired_change_status_to_expired()
        super().save(*args, **kwargs)

    def _verify_if_date_expired_change_status_to_expired(self):
        if self.end_date and self.end_date < timezone.localdate() and self.status == VacationStatus.ACTIVE.name:
            self.status = VacationStatus.EXPIRED.name

    class Meta:
        permissions = []

    @property
    def total_working_day_vacation(self):
        start_working_day, end_working_day = BimaService.get_working_days_for_company()
        return BimaService.working_days_count(self.date_start, self.date_end, start_working_day, end_working_day)
