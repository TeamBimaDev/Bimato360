from common.enums.position import get_seniority_choices
from core.abstract.models import AbstractModel

from django.db import models


class BimaHrPosition(AbstractModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    work_location = models.CharField(max_length=100, blank=True, null=True)
    seniority = models.CharField(max_length=50, choices=get_seniority_choices(), blank=True, null=True)
    requirements = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    department = models.ForeignKey('core.BimaCoreDepartment', on_delete=models.CASCADE, null=True)
    job_category = models.ForeignKey('BimaHrJobCategory', on_delete=models.PROTECT)
    manager = models.ForeignKey('BimaHrEmployee', related_name='directs', blank=True, null=True,
                                on_delete=models.SET_NULL)

    def __str__(self) -> str:
        return f"{self.title, self.department.name}"

    class Meta:
        ordering = ['title']
        permissions = []
        default_permissions = ()
