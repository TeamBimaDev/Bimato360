from common.enums.position import get_contract_type_choices, get_contract_status_choices, ContractType
from common.enums.position import get_termination_reason_choices, get_suspension_reason_choices
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
    termination_reason_type = models.CharField(
        max_length=50,
        choices=get_termination_reason_choices(),
        null=True,
        blank=True,
    )
    suspension_reason_type = models.CharField(
        max_length=50,
        choices=get_suspension_reason_choices(),
        null=True,
        blank=True,
    )
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
    notes = models.TextField(null=True, blank=True)
    new_salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    new_start_date = models.DateField(null=True, blank=True)
    new_end_date = models.DateField(null=True, blank=True)
    other_changes = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=10, choices=get_contract_status_choices())

    def save(self, *args, **kwargs):
        fields_mapping = {
            'new_salary': 'salary',
            'new_start_date': 'start_date',
            'new_end_date': 'end_date',
        }

        for amendment_field, contract_field in fields_mapping.items():
            amendment_value = getattr(self, amendment_field)
            if amendment_value is None or amendment_value == '':
                contract_value = getattr(self.contract, contract_field)
                setattr(self, amendment_field, contract_value)

        super().save(*args, **kwargs)
