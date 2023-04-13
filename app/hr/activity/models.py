from django.db import models
from core.abstract.models import AbstractModel
from hr.activity_type.models import BimaHrActivityType
from hr.applicant.models import BimaHrApplicant


class BimaHrActivity(AbstractModel):
    name = models.CharField(max_length=28, blank=False)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    id_manager = models.IntegerField()
    type_id = models.ForeignKey(BimaHrActivityType, on_delete=models.CASCADE)
    applicant =models.ForeignKey(BimaHrApplicant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.applicant , self.type_id ,self.name}"
