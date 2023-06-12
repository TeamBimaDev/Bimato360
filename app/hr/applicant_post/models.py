from django.db import models
from core.abstract.models import AbstractModel


class BimaHrApplicantPost(AbstractModel):
    expected_salary = models.FloatField(blank=True, null=True, default=None)
    proposed_salary = models.FloatField(blank=True, null=True, default=None)
    accepted_salary = models.FloatField(blank=True, null=True, default=None)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('core.BimaCorePost', on_delete=models.CASCADE)
    applicant = models.ForeignKey('hr.BimaHrApplicant', on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.name, self.public_id}'
