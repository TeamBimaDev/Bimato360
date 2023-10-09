from common.enums.position import get_contract_type_choices, get_contract_status_choices, ContractType
from core.abstract.models import AbstractModel
from django.db import models
from django.utils.translation import gettext_lazy as _
from rest_framework.exceptions import ValidationError
from simple_history.models import HistoricalRecords


class BimaHrContract(AbstractModel):
    employee = models.ForeignKey('BimaHrEmployee', on_delete=models.CASCADE, related_name='contracts')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    contract_type = models.CharField(max_length=16, choices=get_contract_type_choices())
    salary = models.DecimalField(max_digits=10, decimal_places=3)
    note = models.TextField(blank=True, null=True)
    job_description = models.TextField(blank=True, null=True)
    department = models.ForeignKey('core.BimaCoreDepartment', on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(choices=get_contract_status_choices())
    stopped_at = models.DateField(null=True, blank=True)
    reason_stopped = models.CharField(max_length=255, null=True, blank=True)
    manager_who_stopped = models.ForeignKey('BimaHrEmployee', null=True, blank=True, on_delete=models.SET_NULL,
                                            related_name='stopped_contracts')
    probation_end_date = models.DateField(null=True, blank=True)
    exit_notice_date = models.DateField(null=True, blank=True)
    history = HistoricalRecords()

    def __str__(self) -> str:
        return f"{self.employee.full_name} from {self.employee.start_date} type {self.employee.contract_type} status {self.status} "

    def save(self, *args, **kwargs):
        if self.contract_type != ContractType.CDI.name and not self.end_date:
            raise ValidationError({"Date fin": _("End date must be provided for contract types other than CDI")})
        super().save(*args, **kwargs)

    class Meta:
        permissions = []


class BimaHrContractAmendment(AbstractModel):
    contract = models.ForeignKey('BimaHrContract', on_delete=models.CASCADE)
    amendment_date = models.DateField()
    notes = models.TextField()
    new_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_end_date = models.DateField(null=True, blank=True)
    other_changes = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=get_contract_status_choices())

    def save(self, *args, **kwargs):
        for field_name, field_value in self.__dict__.items():
            if field_value is None or field_value == '':
                setattr(self, field_name, getattr(self.contract, field_name))
        super().save(*args, **kwargs)
