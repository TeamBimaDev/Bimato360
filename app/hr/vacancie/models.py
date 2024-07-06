from datetime import date
from django.utils import timezone
from common.enums.position import get_seniority_choices, get_position_status_choices
from core.abstract.models import AbstractModel
from common.enums.employee_enum import get_work_mode_choices, get_job_type_choices
from django.db import models


class BimaHrVacancie(AbstractModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    work_location = models.CharField(max_length=100, blank=True, null=True)
    seniority = models.CharField(max_length=50, choices=get_seniority_choices(), blank=True, null=True)
    department = models.ForeignKey('core.BimaCoreDepartment', on_delete=models.CASCADE, null=True)
    job_category = models.ForeignKey('BimaHrJobCategory', on_delete=models.PROTECT)
    work_mode = models.CharField(max_length=50, choices=get_work_mode_choices(), null=True, blank=True)
    job_type = models.CharField(max_length=50, choices=get_job_type_choices(), null=True, blank=True)
    manager = models.ForeignKey('BimaHrEmployee', related_name='manager', blank=True, null=True,
                                on_delete=models.SET_NULL)
    date_expiration = models.DateField(null=True, blank=True)
    date_start_vacancie = models.DateField(null=True, blank=True)
    number_of_positions = models.FloatField(blank=True, null=True, default=None)
    published_date = models.DateTimeField(auto_now_add=True)
    position_status = models.CharField(max_length=50, choices=get_position_status_choices(), null=True, blank=True)
    candidat_vacancie = models.ManyToManyField('BimaHrCandidat', through='BimaHrCandidatVacancie')
    
    @property
    def number_of_candidates(self):
        return self.candidat_vacancie.count()
    

    def save(self, *args, **kwargs):
        self._verify_and_update_status()
        super().save(*args, **kwargs)

    def _verify_and_update_status(self):
        if self.date_expiration and isinstance(self.date_expiration, date):
          if self.date_expiration and self.date_expiration < timezone.localdate() and self.position_status == 'ACTIVE':
              self.position_status = 'CLOSED'
    
    
    def __str__(self) -> str:
        return f"{self.title, self.department.name}"

    class Meta:
        ordering = ['title']
        permissions = []
        default_permissions = ()
        
        
class BimaHrCandidatVacancie(AbstractModel):
    candidat = models.ForeignKey('BimaHrCandidat', on_delete=models.CASCADE)
    vacancie = models.ForeignKey(BimaHrVacancie, on_delete=models.CASCADE)
    expected_salary = models.FloatField(blank=True, null=True, default=None)
    proposed_salary = models.FloatField(blank=True, null=True, default=None)
    accepted_salary = models.FloatField(blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    comments = models.TextField(max_length=256)
    score = models.FloatField(null=True, blank=True, default=None)