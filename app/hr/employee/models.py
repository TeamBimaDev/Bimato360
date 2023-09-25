from common.enums.employee_enum import get_marital_status_choices, get_employment_type_choices, \
    get_work_mode_choices, get_job_type_choices, get_employee_status_choices
from django.db import models
from hr.models import BimaHrPerson

from hr.position.models import BimaHrPosition


class BimaHrEmployee(BimaHrPerson):
    marital_status = models.CharField(max_length=20, choices=get_marital_status_choices(), null=True, blank=True)
    num_children = models.IntegerField(default=0, null=True, blank=True)
    employment_type = models.CharField(max_length=20, choices=get_employment_type_choices())
    work_mode = models.CharField(max_length=20, choices=get_work_mode_choices())
    job_type = models.CharField(max_length=20, choices=get_job_type_choices())
    employment_status = models.CharField(max_length=20, choices=get_employee_status_choices())
    probation_end_date = models.DateField(null=True, blank=True)
    last_performance_review = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=3, null=True, blank=True)
    position = models.OneToOneField(BimaHrPosition, related_name='employee', blank=True, null=True,
                                    on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.first_name, self.last_name}"

    class Meta:
        ordering = ['first_name']
        permissions = []
        default_permissions = ()
