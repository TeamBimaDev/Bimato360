from datetime import datetime

from common.enums.employee_enum import get_employment_type_choices, \
    get_work_mode_choices, get_job_type_choices, get_employee_status_choices
from common.validators.date_format_validator import DateFormatValidator
from django.db import models
from hr.models import BimaHrPerson
from hr.position.models import BimaHrPosition
from simple_history.models import HistoricalRecords


class BimaHrEmployee(BimaHrPerson):
    employment_type = models.CharField(max_length=20, choices=get_employment_type_choices(), null=True, blank=True)
    work_mode = models.CharField(max_length=20, choices=get_work_mode_choices(), null=True, blank=True)
    job_type = models.CharField(max_length=20, choices=get_job_type_choices(), null=True, blank=True)
    employment_status = models.CharField(max_length=20, choices=get_employee_status_choices(), null=True, blank=True)
    hiring_date = models.DateField(null=True, blank=True, validators=[DateFormatValidator.validate])
    probation_end_date = models.DateField(null=True, blank=True, validators=[DateFormatValidator.validate])
    last_performance_review = models.DateField(null=True, blank=True, validators=[DateFormatValidator.validate])
    salary = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    position = models.ForeignKey(BimaHrPosition, blank=True, null=True, on_delete=models.SET_NULL)
    balance_vacation = models.FloatField(default=0)
    virtual_balance_vacation = models.FloatField(default=0)
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.first_name, self.last_name}"

    def save(self, *args, **kwargs):
        self.clean_dates()
        super().save(*args, **kwargs)

    def clean_dates(self):
        date_fields = ['last_performance_review', 'probation_end_date', 'hiring_date']
        for field_name in date_fields:
            date_value = getattr(self, field_name)
            if date_value:
                try:
                    datetime.strptime(str(date_value), '%Y-%m-%d')
                except ValueError:
                    setattr(self, field_name, None)

    class Meta:
        ordering = ['first_name']
        permissions = []
        default_permissions = ()
